import study as study_mod
import sys

study = study_mod.Study('main.db')

study.delete_quiz(sys.argv[1])
