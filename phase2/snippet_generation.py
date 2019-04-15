from bs4 import BeautifulSoup


def word_in_query(query, word):
    for term in query.split():
        if word == term:
            return True
    return False

def get_summary(filename, query):
    f_open = open(filename, 'r')
    bs = BeautifulSoup(f_open, 'html.parser')
    content = []
    for pre in bs.find_all(['pre']):
        content.append(pre.text)
    lowered_sentence = ' '.join(content).lower()
    check_am = lowered_sentence.split('am')
    if len(check_am) > 1:
        lowered_sentence = "am".join(check_am[:-1]) + " am"
    check_pm = lowered_sentence.split('pm')
    if len(check_pm) > 1:
        lowered_sentence = "pm".join(check_pm[:-1]) + " pm"
    new_sentence = " ".join(" ".join(lowered_sentence.split("\n")).split()).split(".")
    sentence_score = {}
    for sentence in new_sentence:
        sentence_score[sentence] = get_significance_factor(query, sentence)
    count = 1
    summary = []
    zerovaluenum = 0
    for i in sorted(sentence_score, key=sentence_score.get, reverse=True):
        if sentence_score[i] == 0:
            zerovaluenum += 1
        if count < 6 and zerovaluenum < 3:
            summary.append(str(i))
            count += 1
    return summary

def get_significance_factor(query, sentence):
    words = sentence.split()
    lowpos = 0
    hipos = 0
    count = 0
    for k in range(len(words)):
        if word_in_query(query, words[k]):
            lowpos = k
            break
    for i in range(len(words) - 1, 0, -1):
        if word_in_query(query, words[i]):
            hipos = i
            break
    for w in words[lowpos: (hipos + 1)]:
        if word_in_query(query, w):
            count += 1
    if len(words[lowpos: (hipos + 1)]) == 0:
        factor = 0
    else:
        factor = (count ** 2) / len(words[lowpos: (hipos + 1)])

    return factor


def get_snippet(filename, query, ranking, f):
    query = query.lower()
    summary = get_summary(filename, query)
    # f = open("snippets.html", 'w')
    system_output = ""
    html_output = ""
    filename = filename.split('/')[-1]
    print(ranking+"\n")
    print("Filename: "+'\033[1m' + '\033[94m' + filename + '\033[0m'+ "        QUERY: " '\033[1m' + '\033[91m' + query +
          '\033[0m')
    print("<html><p>" + ranking + "</p>", file=f)
    print("<p>" + "Filename: " + '<font color="blue">' + filename + '</font>' + "        QUERY: " + '<font color="red">' + query +
        '</font>'+ "</p>", file=f)
    print("-------------------------------------------------------------------------------------------------")
    print("<p>-------------------------------------------------------------------------------------------------</p>", file=f)
    for sentence in summary:
        html_output += "<p>******"
        system_output += "******"
        for word in str(sentence).split():
            if word_in_query(query, word):
                system_output += '\033[1m' + '\033[95m' + word + '\033[0m' + " "
                html_output += '<font color="red">' + word + '</font>' + " "
            else:
                system_output += word + " "
                html_output += word + " "
        system_output += ".\n"
        html_output += ".</p>"
    print(system_output)
    print(html_output, file=f)
    print("==================================================================================================")
    print("<p>===============================================================================================</p></html>",file=f)

if __name__ == '__main__':
    get_snippet("../test-collection/cacm/CACM-3189.html", "FORTRAN Program", "", "snippets.html")
