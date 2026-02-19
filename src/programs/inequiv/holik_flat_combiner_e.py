from src.GenerateFunctions import h4
from src.UniversalStrategy import make_function_equivalence_test


def holik_flat_combiner_e_lhs():
    list_ref = [lambda x: None]
    cnt = [0]
    running = [0]

    def enlist(f):
        if not (running[0] == 0):
            pass
        else:
            cnt[0] = cnt[0] + 1
            c = cnt[0]
            l = list_ref[0]
            list_ref[0] = lambda z: f() if z == c else l(z)

    def run():
        running[0] = 1
        if 0 < cnt[0]:
            list_ref[0](cnt[0])
            cnt[0] = cnt[0] - 1
            if cnt[0] < 0:
                raise Exception("_bot_")
            run()
        else:
            list_ref[0] = lambda x: None
            running[0] = 0

    return lambda f: f(enlist)(run)


def holik_flat_combiner_e_rhs():
    list_ref = [lambda x: None]
    cnt = [0]
    running = [0]

    def enlist(f):
        if not (running[0] == 0):
            pass
        else:
            cnt[0] = cnt[0] + 1
            c = cnt[0]
            l = list_ref[0]
            list_ref[0] = lambda z: f() if z == c else l(z)

    def run():
        running[0] = 1

    return lambda f: f(enlist)(run)

test_holik_flat_combiner_e \
    = make_function_equivalence_test(holik_flat_combiner_e_lhs,
                                     holik_flat_combiner_e_rhs,
                                     log_failure=True)

# on the lhs, enlist takes a function and essentially adds that function to
# a linked list of functions while run runs each function in the list

# on rhs, enlist does the same but run lacks the logic, it runs nothing

# example of a function that causes differing behaviour
def f(enlist):
    x = {"value": 0}

    def task():
        x["value"] = 1

    enlist(task)

    def k(run):
        run()
        return x["value"]

    return k

# more generally, see the definition of f in GenerateFunctions.create_curried_interaction
