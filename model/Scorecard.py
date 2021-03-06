from collections import namedtuple
import re

from util import float_of

Element = namedtuple('Element', ['number',       # order in program
                                 'name',         # e.g. 3A
                                 'info',         # e.g. UR
                                 'base_value',   # float
                                 'bonus',
                                 'goe',          # aggregated over judges
                                 'goes',         # list of individual judge GOEs (-3 to 3)
                                 'parsed_goes',  # goes with - removed
                                 'points'])      # total points for element

ProgramComponent = namedtuple('ProgramComponent', ['name',    # e.g. 'Skating Skills'
                                                   'factor',  # e.g. 1.0 in men's short, 2.0 in men's free
                                                   'scores',  # list of individual judge's scores
                                                   'parsed_scores',  # scores with - removed
                                                   'points']) # aggregated judge's scores multiplied by factor

class Scorecard:
    def __init__(self, url, season, event, discipline, segment, skater,
                 rank, starting_number, total_score, tes, pcs, deductions):
        self.url = url
        self.season = season
        self.event = event
        self.discipline = discipline
        self.segment = segment
        self.skater = skater
        self.rank = int(rank)
        try:
            self.starting_number = int(starting_number)
        except:
            self.starting_number = 0
        self.tes = float_of(tes)
        self.pcs = float_of(pcs)
        self.total_deductions = float_of(deductions)
        self.total_score = float_of(total_score)
        self.base_value = 0.00

        self.elements = []
        self.components = []
        self.deductions = {}

        self.extra_judges = 0
        self.mistakes = []
        self.pre10 = int(self.season.champ_year) <= 2010

    def __repr__(self):
        return '{0}: {1}, {2} + {3} - {4} = {5}'.format(
            self.segment, self.skater,
            self.tes, self.pcs, self.total_deductions, self.total_score)
        
    def add_element(self, elt_match):
        number, name, info, base_value, bonus, goe, goes, extra, points = elt_match.groups()
        number = int(number)
        base_value = float_of(base_value)
        bonus = bonus != ''
        goe = float_of(goe)

        # Split out individual judges' GOEs
        goe_re = re.compile('(-?\d|-)')
        goe_match = goe_re.findall(goes)
        if not goe_match:
            raise Exception(goes)

        if self._is_zeroed_element(base_value):
            goes = [0.00 for _ in xrange(len(goe_match))]
            parsed_goes = goes
        else:
            goes, parsed_goes = self._parse_goes(goe_match)

        if not self.pre10 and extra and self._is_first_elt_of_segment():
            self.mistakes.append('Extra Judges: ' + extra)

        points = float_of(points)
        self.elements.append(Element(number, name, info, base_value, bonus, goe, goes, parsed_goes, points))

    def add_component(self, component_match):
        name, factor, scores, points = component_match.groups()
        factor = float_of(factor)
        comp_mark_re = re.compile('(\d?\d.\d\d|-)\s*')
        comp_match = comp_mark_re.findall(scores)
        if not comp_match:
            raise Exception(scores)
        scores, parsed_scores = self._parse_components(comp_match)

        points = float_of(points)
        self.components.append(ProgramComponent(name.strip(), factor, scores, parsed_scores, points))

    def add_deduction(self, deductions):
        for deduction in deductions:
            if ':' in deduction:
                reason, value = deduction.split(':')
            else:
                reason, value = deduction.split()
            fall_re = re.compile('(-\d.\d\d)\s*(\(\d\))')
            if fall_re.match(value):
                value, num_falls = fall_re.match(value).groups()
                reason += num_falls
            value = float_of(value)
            if value > 0.:      # Sometimes deductions are captured as positive.
                value = -value

            # Ignore deductions of zero value.
            if not self._is_close(0.00, value):
                self.deductions[reason.strip()] = value
    
    def aggregate_elements(self, tes_match):
        self.base_value, tes = map(float_of, tes_match.groups())
        self._check(tes, self.tes, 'two summary tes match')
        self._check_elements()

    def _check_elements(self):
        if not self.elements:
            raise Exception('{0} has no technical elements in {1}.'.format(self, self.segment))
        self.goe_total = sum([elt.goe for elt in self.elements])
        for (num1, num2, description) in (
            (sum([elt.base_value for elt in self.elements]), self.base_value, 'base value total'),
            (self.goe_total, self.tes - self.base_value, 'base value + goe total = tes'),
            (sum([elt.points for elt in self.elements]), self.tes, 'sum of elts = tes'),
            ):
            self._check(num1, num2, description)

        # Check the GOEs for sanity.
        for i, elt in enumerate(self.elements):
            self._check(elt.base_value + elt.goe, elt.points, 
                        'bv + goe = elt points ' + str(i+1))

    def aggregate_pcs(self, pcs):
        self._check(float_of(pcs), self.pcs, 'two summary pcs match')
        self._check_pcs()

    def _check_pcs(self):
        if not self.components:
            raise Exception('{0} has no components.'.format(self, self.segment))
        pcs_count = 0.
        for component in self.components:
            points = (sum(component.parsed_scores) - min(component.parsed_scores) - max(component.parsed_scores)) / (len(component.parsed_scores) - 2)
            self._check(points, component.points, 'aggregated component: ' + component.name, True)
            pcs_count += round(points, 2) * component.factor
        if self.pre10:
            pcs_count = sum([comp.points * comp.factor for comp in self.components])
        self._check(pcs_count, self.pcs, 'summary pcs = computed pcs')

    def check_total(self):
        self._check(self.tes + self.pcs + sum(self.deductions.values()),
                    self.total_score, 'total score')
        self._check_elements()
        self._check_pcs()
        if self.extra_judges:
            self.mistakes.append('{0} extra judges: {1}'
                .format(self.extra_judges,
                        [judge for judge, goe in enumerate(self.elements[0].goes) if goe == '-'])
                )
        return self.mistakes

    def print_scorecard(self):
        print self.skater, self.rank, 'start:', self.starting_number
        print 'TES: {0}, PCS: {1}, Total: {2}'.format(self.tes, self.pcs, self.total_score)
        print 'Deductions: ' + str(self.deductions)
        for element in self.elements:
            print element
        for component in self.components:
            print component

    def _is_close(self, float1, float2):
        return abs(float1 - float2) < 0.03

    def _check(self, num1, num2, description, no_check_pre10=False):
        if not (self.pre10 and no_check_pre10) and not self._is_close(num1, num2):
            self.mistakes.append('{0}: {1}, {2} != {3}'.format(self.skater, num1, num2, description))

    def _parse_goes(self, goe_match):
        """Sometimes judges are removed, resulting in a - for a GOE."""
        goes = []
        parsed_goes = []
        extra_judges = 0
        for goe in goe_match:
            try:
                goes.append(int(goe))
                parsed_goes.append(int(goe))
            except:
                # This guy's scorecard is weird.
                if self.skater.name == 'Harry Hau Yin LEE' and self.event.name == 'fc2015':
                    goes.append(0)
                    parsed_goes.append(0)
                else:
                    goes.append('-')
                    extra_judges += 1
        if not self.elements:       # First element of this scorecard.
            self.extra_judges = extra_judges
        self._check(self.extra_judges, extra_judges, 'check consistency of # extra judges')
        return goes, parsed_goes

    def _parse_components(self, comp_match):
        """When a judge is removed, the component mark becomes 0.00 or -."""
        scores = []
        parsed_scores = []
        extra_judges = 0
        for score_str in comp_match:
            try:
                score = float_of(score_str)
                if self._is_close(0.00, score):
                    extra_judges += 1
                    scores.append('-')
                else:
                    scores.append(score)
                    parsed_scores.append(score)
            except:
                extra_judges += 1
                scores.append('-')
        self._check(self.extra_judges, extra_judges, 'pcs extra judges = tes extra judges')
        return scores, parsed_scores

    def _is_first_elt_of_segment(self):
        return not self.elements and self.rank == 1

    def _is_zeroed_element(self, base_value):
        """Sometimes a skater receives no credit for an element when it is invalidated."""
        return self._is_close(0.00, base_value)
