"""
Form Validation Module
"""

# local Django
from app.modules.validation.validator import Validator
from app.modules.validation.sanitizer import Sanitizer
from app.exceptions.sanitization_rule_not_found import Sanitization_Rule_Not_Found
from app.exceptions.validation_rule_not_found import Validation_Rule_Not_Found


class Form():

    __inputs = {}
    __errors = {}

    __vstatus = False
    __sstatus = False

    __validator = None
    __sanitizer = None
    __sanitizers = []
    __validators = []

    def __init__(self, inputs={}):
        self.__inputs = inputs
        self.__validator = Validator()
        self.__sanitizer = Sanitizer()

    def add_inputs(self, inputs={}):
        self.__inputs = inputs

    def get_inputs(self):
        return self.__inputs

    def get_input_value(self, input_key, sanitized=True):
        return self.__inputs[input_key]["value"] if not sanitized or "svalue" not in self.__inputs[input_key] else self.__inputs[input_key]["svalue"]

    def get_errors(self, with_type=False):
        if with_type:
            errors = []
            for input_key, error_list in self.__errors.items():
                for error in error_list:
                    errors.append({"type": "error", "message": error})
            return errors
        else:
            return self.__errors

    def is_passed(self):
        for input in self.__inputs:
            if len(self.__errors[input]) > 0:
                return False
        return True

    def get_vstatus(self):
        return self._vstatus

    def get_sstatus(self):
        return self._sstatus

    def process(self, direction=['sanitize', 'validate']):
        if direction[0] == 'sanitize':
            if 'sanitize' in direction:
                self.__sanitize()
            if 'validate' in direction:
                self.__validate()
        else:
            if 'validate' in direction:
                self.__validate()
            if 'sanitize' in direction:
                self.__sanitize()

    def add_validator(self, val_instance):
        self.__validators.append(val_instance)

    def add_sanitizer(self, san_instance):
        self.__sanitizers.append(san_instance)

    def __validate(self):
        status = True

        for current_input, validation_rule in self.__inputs.items():
            self.__validator.set_input(self.__inputs[current_input]['value'])
            if 'validate' in validation_rule:
                self.__errors[current_input] = []
                for rule_name, rule_args in validation_rule['validate'].items():
                    self.__update_validator(rule_name)
                    # Check if param exist and pass them to the method
                    if 'param' in rule_args.keys() and len(rule_args['param']) > 0:
                        current_status = getattr(self.__validator, rule_name)(*rule_args['param'])
                    else:
                        current_status = getattr(self.__validator, rule_name)()

                    if "optional" in validation_rule['validate'] and self.__inputs[current_input]['value'] == "":
                        current_status = True

                    self.__inputs[current_input]['status'] = current_status
                    status &= current_status
                    if not current_status and 'error' in rule_args.keys():
                        self.__errors[current_input].append(rule_args['error'])

        self.__vstatus = status
        return status

    def __sanitize(self):
        status = True
        for current_input, sanitization_rule in self.__inputs.items():
            self.__sanitizer.set_input(self.__inputs[current_input]['value'])
            self.__sanitizer.set_sinput(None)
            if 'sanitize' in sanitization_rule:
                for rule_name, rule_args in sanitization_rule['sanitize'].items():
                    self.__update_sanitizer(rule_name)
                    # Check if param provided and pass them to the method
                    if 'param' in rule_args.keys() and len(rule_args['param']) > 0:
                        sanitized_value = getattr(self.__sanitizer, rule_name)(*rule_args['param'])
                    else:
                        sanitized_value = getattr(self.__sanitizer, rule_name)()
                    self.__inputs[current_input]['svalue'] = sanitized_value
                    self.__inputs[current_input]['is_exact'] = True if self.__inputs[current_input]['value'] == self.__sanitizer.get_sinput() else False
                    status &= self.__inputs[current_input]['is_exact']

        self.__sstatus = status
        return status

    def __update_validator(self, rule_name):
        if hasattr(self.__validator, rule_name):
            return True
        for validator in self.__validators:
            if hasattr(validator, rule_name):
                self.__validator = validator
                return True
        raise Validation_Rule_Not_Found('Non existent validation rule %s' % rule_name)

    def __update_sanitizer(self, rule_name):
        if hasattr(self.__sanitizer, rule_name):
            if self.__sanitizer.get_sinput() is None:
                self.__sanitizer.set_input(self.__sanitizer.get_input())
                self.__sanitizer.set_sinput(None)
            else:
                self.__sanitizer.set_input(self.__sanitizer.get_sinput())
            return True
        for sanitizer in self.__sanitizers:
            if hasattr(sanitizer, rule_name):
                if self.__sanitizer.get_sinput() is None:
                    sanitizer.set_input(self.__sanitizer.get_input())
                    sanitizer.set_sinput(None)
                else:
                    sanitizer.set_input(self.__sanitizer.get_sinput())
                self.__sanitizer = sanitizer
                return True
        raise Sanitization_Rule_Not_Found('Non existent sanitization rule %s' % rule_name)
