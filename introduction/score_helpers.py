def get_grade(score):
    if score >= 90:
        grade = "A"
    else:
        if score >= 80:
            grade = "B"
        else:
            if score >= 70:
                grade = "C"
            else:
                if score >= 60:
                    grade = "D"
                else:
                    grade = "F"
    return grade


def filter_passing(results):
    passing = []
    for r in results:
        if r["score"] >= 60:
            passing.append(r)
        else:
            pass
    return passing


def has_failures(results):
    count = 0
    for r in results:
        if r["score"] < 60:
            count = count + 1
    if count > 0:
        return True
    else:
        return False


def names(results):
    out = []
    for i in range(0, len(results)):
        out.append(results[i]["name"])
    return out
