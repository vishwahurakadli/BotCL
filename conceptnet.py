import data_utils
import conceptset_utils

"""
ConceptNet params:
LIMIT:how many relations to look up, higher limit -> larger concept set
RELATIONS: which relations to include in search 

filters:
CLASS_SIM_CUTOFF: Concenpts with cos similarity higher than this to any class will be removed
OTHER_SIM_CUTOFF: Concenpts with cos similarity higher than this to another concept will be removed
MAX_LEN: max number of characters in a concept

PRINT_PROB: what percentage of filtered concepts will be printed

"""

LIMIT = 200
RELATIONS = ["HasA", "IsA", "PartOf", "HasProperty", "MadeOf"]#, "AtLocation"]

CLASS_SIM_CUTOFF = 0.85
OTHER_SIM_CUTOFF = 0.9 
MAX_LEN = 30

PRINT_PROB = 0.2

dataset = str(input("Dataset: "))
save_name = 'data/concept_sets/conceptnet_{}_filtered_new.txt'.format(dataset)

cls_file = data_utils.LABEL_FILES[dataset]

with open(cls_file, 'r') as f:
    classes = f.read().split('\n')

# Collect initial concepts

concepts = conceptset_utils.get_init_conceptnet(classes, LIMIT, RELATIONS)

concepts = conceptset_utils.remove_too_long(concepts, MAX_LEN, PRINT_PROB)

# Filter out concepts too similar to class names

concepts = conceptset_utils.filter_too_similar_to_cls(concepts, classes, CLASS_SIM_CUTOFF, print_prob=PRINT_PROB)

# Filter out concepts too similar to each other

concepts = conceptset_utils.filter_too_similar(concepts, OTHER_SIM_CUTOFF, print_prob=PRINT_PROB)

print(len(concepts))