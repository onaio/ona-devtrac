TYPE_FIELDTRIP = 'fieldtrip'
TYPE_PLACE = 'place'
QUESTIONNAIRE_SUBMIT_API_PATH = 'api/questionnaire/submit'

questions = {}
questions["q_402"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_404"] = {"type": "number"}
questions["q_405"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_406"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_407"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_408"] = {"type": "number"}
questions["q_409"] = {"type": "number"}
questions["q_410"] = {"type": "number"}
questions["q_411"] = {"type": "number"}
questions["q_412"] = {"type": "number"}
questions["q_413"] = {"type": "number"}
questions["q_414"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_416"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_417"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_418"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_419"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_420"] = {"type": "number"}
questions["q_421"] = {"type": "number"}
questions["q_422"] = {"type": "number"}
questions["q_423"] = {"type": "number"}
questions["q_424"] = {"type": "number"}
questions["q_425"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_426"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_427"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_430"] = {"type": "number"}
questions["q_431"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_432"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_434"] = {"type": "number"}
questions["q_435"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_437"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_439"] = {"type": "checkboxes"}
questions["q_443"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_472"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_473"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_474"] = {"type": "select"}
questions["q_475"] = {"type": "checkboxes"}
questions["q_476"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_477"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_478"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_479"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_480"] = {"type": "number"}
questions["q_481"] = {"type": "number"}
questions["q_482"] = {"type": "number"}
questions["q_483"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_484"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_485"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_486"] = {"type": "radios"}
questions["q_487"] = {"type": "number"}
questions["q_488"] = {"type": "checkboxes"}
questions["q_489"] = {"type": "number"}
questions["q_490"] = {"type": "number"}
questions["q_491"] = {"type": "number"}
questions["q_492"] = {"type": "number"}
questions["q_493"] = {"type": "checkboxes"}
questions["q_494"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_495"] = {"type": "select"}
questions["q_496"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_497"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_498"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_499"] = {"type": "select"}
questions["q_500"] = {"type": "number"}
questions["q_501"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_502"] = {"type": "checkboxes"}
questions["q_503"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_504"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_505"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}
questions["q_506"] = {"type": "radios", "options": {"yes": "Yes", "no": "No"}}

questions["q_474"]["options"] = {}
questions["q_474"]["options"]["one_month_or_less"] = "Less than 1 month ago"
questions["q_474"]["options"]["one_to_six_months"] = "1-6 months ago"
questions["q_474"]["options"]["more_than_six_months"] = "More than 6 months ago"  # noqa


questions["q_439"]["options"] = {}
questions["q_439"]["options"]["protected_spring"] = "Protected spring"
questions["q_439"]["options"]["piped_water_scheme"] = "Piped water scheme"
questions["q_439"]["options"]["hand_pump"] = "Hand pump"

questions["q_475"]["options"] = {}
questions["q_475"]["options"]["in_charge"] = "In-charge"
questions["q_475"]["options"]["doctor"] = "Doctor"
questions["q_475"]["options"]["nurse"] = "Nurse"
questions["q_475"]["options"]["health_assistant"] = "Health Assistant"
questions["q_475"]["options"]["records_officer"] = "Records Officer"


questions["q_486"]["options"] = {}
questions["q_486"]["options"]["yes"] = "Yes"
questions["q_486"]["options"]["no"] = "No"
questions["q_486"]["options"]["na_there_is_no_book"] = "N/a - there is no book"

questions["q_488"]["options"] = {}
questions["q_488"]["options"]["mre_classroom_discussions"] = "MRE classroom discussions"  # noqa
questions["q_488"]["options"]["mre_materials"] = "MRE materials: posters, leaflets"  # noqa
questions["q_488"]["options"]["mre_messages_around_schools"] = "MRE messages around schools"  # noqa
questions["q_488"]["options"]["none_of_the_above"] = "None of the above"

questions["q_493"]["options"] = {}
questions["q_493"]["options"]["police"] = "Police"
questions["q_493"]["options"]["health_centre"] = "Health Centre"
questions["q_493"]["options"]["child_protection_committe"] = "Child Protection Committee"  # noqa
questions["q_493"]["options"]["probation_officer"] = "Probation Officer"
questions["q_493"]["options"]["lc"] = "LC"
questions["q_493"]["options"]["other"] = "Other"
questions["q_493"]["options"]["dont_know"] = "Don't know"

questions["q_495"]["options"] = {}
questions["q_495"]["options"]["protected_spring"] = "Protected spring"
questions["q_495"]["options"]["piped_water_scheme"] = "Piped water scheme"
questions["q_495"]["options"]["borehole_with_handpump"] = "Borehole with handpump"  # noqa
questions["q_495"]["options"]["shallow_well_with_handpump"] = "Shallow well with handpump"  # noqa

questions["q_499"]["options"] = {}
questions["q_499"]["options"]["contaminated"] = "Contaminated"
questions["q_499"]["options"]["not_contaminated"] = "Not contaminated"
questions["q_499"]["options"]["unable_to_test"] = "Unable to test"

questions["q_502"]["options"] = {}
questions["q_502"]["options"]["yes"] = "Yes"
questions["q_502"]["options"]["no"] = "No"
questions["q_502"]["options"]["na_no_child_was_sick"] = "N/a - no child was sick"  # noqa
