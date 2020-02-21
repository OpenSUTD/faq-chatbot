import requests
import csv

response_official = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJhneAPMMIDOFC_lEGOz9hcdMO8ZaDwoKgd8HlqISYSJGWcR-Yy_zGnOhvjuQqr_1rnMihRR8Uy9AV/pub?output=csv"
)
csv_name_official = "official_faq.csv"
response_student = requests.get(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTJhneAPMMIDOFC_lEGOz9hcdMO8ZaDwoKgd8HlqISYSJGWcR-Yy_zGnOhvjuQqr_1rnMihRR8Uy9AV/pub?gid=1618586175&single=true&output=csv"
)
csv_name_student = "student_faq.csv"

synonyms = {
    "ISTD": [
        "Information Systems Technology and Design",
        "Information Systems Technology and Design pillar",
        "ISTD pillar",
    ],
    "EPD": [
        "Engineering Product Development",
        "Engineering Product Development pillar",
        "EPD pillar",
    ],
    "ESD": [
        "Engineering Systems and Design",
        "Engineering Systems and Design pillar",
        "ESD pillar",
    ],
    "ASD": [
        "Architecture and Sustainable Design",
        "Architecture and Sustainable Design Pillar",
        "ASD pillar",
        "archi",
        "architecture",
    ],
    "DAI": [
        "Design and Artificial Intelligence",
        "Design and Artificial Intelligence pillar",
        "DAI pillar",
    ],
    "SHARP": [
        "SUTD Honours and Research Programme",
        "Honours and Research programme",
        "Honours and Research Program",
    ],
    "ILP": ["Integrated Learning Programme"],
    "IAP": ["Independent Activities Period"],
}


def change_syn(response, csv_name):
    content = response.content.decode("utf-8")
    # print(content)

    with open(csv_name, mode="w", encoding="utf-8") as faq_csv:
        csv_writer = csv.writer(faq_csv, delimiter=",", quotechar='"')
        for i in content.split("\n"):
            replace = []
            try:
                question = (i.split(',"')[0]).replace('"', "")
                answer = (i.split(',"')[1]).replace('"', "")
            except:
                if i[-1] == '"':
                    question = (i.split(",")[0]).replace('"', "")
                    answer = (i.split(",")[1]).replace('"', "")
                else:
                    question = (i.rsplit(",", 1)[0]).replace('"', "")
                    answer = (i.rsplit(",", 1)[1]).replace('"', "")
            for word in question.split(" "):
                if len(word) > 1:
                    if word[-1] == "?" or word[-1] == ",":
                        word = word[:-1]
                    if word in synonyms.keys():
                        replace.append(word)
            if len(replace) != 0:

                for replace_word in replace:
                    for value in synonyms[replace_word]:
                        new_question = question.replace(replace_word, value)
                        csv_writer.writerow([new_question, answer])
            csv_writer.writerow([question, answer])


change_syn(response_official, csv_name_official)
change_syn(response_student, csv_name_student)
