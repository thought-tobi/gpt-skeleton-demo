import difflib as dl


def diff(a, b):
    d = dl.Differ()
    return clean_diff(list(d.compare(a.split(), b.split())))


def clean_diff(diffs: list[str]) -> list:
    return [diff.strip() for diff in diffs if not diff.startswith('?')]


if __name__ == '__main__':
    print(diff("The format for this retrospective isn't quite clear at the moment.",
                    "The format for this retrospective is not yet clear."))
