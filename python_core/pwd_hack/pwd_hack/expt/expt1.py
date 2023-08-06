# orig_str = "old macdonald had an old farm"
# orig_ind = orig_str.split().index("old")
# orig_str_list = orig_str.split()
# orig_str_list.reverse()
# new_str = ' '.join(orig_str_list)
# rev_ind = (sum(len(i) for i in orig_str_list[:(orig_str_list.index("old"))]) +
#            (len(orig_str_list[:(orig_str_list.index("old"))])))
# print(max(orig_ind, rev_ind))


def get_idx_word(sentence: str, word: str = "old") -> int:
    sentence_list = sentence.split()
    return (sum(len(i) for i in sentence_list[:(sentence_list.index(word))]) +
            (len(sentence_list[:(sentence_list.index(word))])))


def get_rev_sentence(sentence: str) -> str:
    s_list = sentence.split()
    s_list.reverse()
    return " ".join(s_list)


if __name__ == '__main__':
    s = "old macdonald had an old farm"
    # print(get_idx_word(sentence=get_rev_sentence(sentence=s)))
    s_front_idx = s.index("old")

    # s_back_idx1 = s.index("old", s[len(s) - 1], s[0])
    # print(s_back_idx1)

    s_back_idx = (len(s) - s_front_idx) - 1
    # print(s_front_idx, s_back_idx, len(s))
    print(s.rfind("old"))


# Read the input, find the starting index of the substring old, then search backward from the end of the string for the same substring, and print the bigger value of the two.