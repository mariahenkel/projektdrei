from pprint import pprint
from mendeley_client import *
import operator
import numpy as np
from matplotlib import pyplot as p
from datetime import datetime
import json


def save_as_pickle(p_object, filename):
    with open("%s.pk" % filename, "wb") as p_output:
        pickle.dump(p_object, p_output, pickle.HIGHEST_PROTOCOL)


def open_from_pickle(filename):
    with open("%s.pk" % filename, "rb") as p_input:
        r_object = pickle.load(p_input)
    return r_object


if __name__ == "__main__":


    # ### Collect the required data ###

    # mendeley = create_client()
    # categories = mendeley.categories()

    # Export all categories for later usage
    # with open("categories.json", "wb") as json_output:
    #     json.dump(categories, json_output, indent=4)

    # Overall publications publications of all time
    # overall_pub = {}
    # for i in range(2003, 2013):
    #     overall_pub[i]=mendeley.search("year:%s"%i)["total_results"]

    # # Top 20 Tags from Computer and Information Science (cat 6)
    # top20tags = mendeley.tag_stats(6)

    # All publications by the author Wolfgang G Stock
    # pub_stock = mendeley.search("author:\"Wolfgang G Stock\"", items=500)

    # Top 10 publications published in "Nature"
    # top10_nature = mendeley.search("published_in:\"Nature\"", items=10)

    # All Publications with the tag "ontology"
    # onto_tagged = {}
    # for category in categories:
    #     onto_tagged[category["id"]] = 0
    #     page_count = mendeley.tagged("ontology", items=500)["total_pages"]
    #     for page_num in range(1, page_count+1):
    #         tagged = mendeley.tagged("ontology", items=500, page=page_num)
    #         for document in tagged["documents"]:
    #             if document["year"]==2011:
    #                 onto_tagged[category["id"]] += 1


    # ### Save the collected data in pickle files ###

    # save_as_pickle(overall_pub, "overall_pub")
    # save_as_pickle(top20tags, "top20tags")
    # save_as_pickle(pub_stock, "pub_stock")
    # save_as_pickle(top10_nature, "top10_nature")
    # save_as_pickle(onto_tagged, "onto_tagged")
    # pprint (open_from_pickle("top10_nature")["documents"])


    # ### Plotting ###

    # Top20 Tags
    # tags = open_from_pickle("top20tags")
    # tags_value = []
    # tags_name = []
    # for element in tags:
    #   tags_value.append(element["count"])
    #   tags_name.append(element["name"].encode("utf-8"))
    # ind=range(len(tags_value))
    # fig = p.figure()
    # ax = fig.add_subplot(1,1,1)
    # ax.bar(ind, tags_value, align='center')
    # ax.set_ylabel('Anzahl')
    # ax.set_title("Top20 Tags der Kategorie 'Computer and Informationscience'")
    # ax.set_xticks(ind)
    # ax.set_xticklabels(tags_name)
    # fig.autofmt_xdate()
    # p.show()

    """
    # Overall Publications
    publications = open_from_pickle("overall_pub")
    sizes = []
    t = 0
    pub_years = {}
    pub_syears = []
    pub_scount = []
    for element in publications:
        if element["year"] >=2003:
            if element["year"] in pub_years:
                pub_years[element["year"]] += 1
            else:
                pub_years[element["year"]] = 1
    sorted_years = sorted(pub_years.iteritems(), key=operator.itemgetter(0))
    for element in sorted_years:
        pub_syears.append(element[0])
        pub_scount.append(element[1])
    for element in pub_scount:
        t = t+element
    for element in pub_scount:
        x = (float(element)/t)*100
        sizes.append(x)
    p.pie(sizes, labels=pub_syears, autopct='%1.1f%%', startangle=90)
    p.axis('equal')
    p.show()
    """
    """
    # Stock Publications/Year
    publications = open_from_pickle("pub_stock")
    pub_years = []
    pub_dic = {}
    all_years = []
    pub_syears = []
    pub_scount = []
    for element in publications["documents"]:
        pub_years.append(element["year"])
    pub_years=sorted(pub_years)
    for i in range(pub_years[0], pub_years[-1]):
        all_years.append(i)
    for year in all_years:
        if year in pub_years:
            for element in publications["documents"]:
                if year==element["year"]:
                    if element["year"] in pub_dic:
                        pub_dic[element["year"]] += 1
                    else:
                        pub_dic[element["year"]] = 1
        else:
            pub_dic[year] = 0
    sorted_years = sorted(pub_dic.iteritems(), key=operator.itemgetter(0))
    for element in sorted_years:
        pub_syears.append(datetime.strptime(str(element[0]) , '%Y'))
        pub_scount.append(element[1])
    p.plot_date(x=pub_syears, y=pub_scount, fmt="-")
    p.ylabel("Publications")
    p.title("Number of Publications/year from Wolfgang G. Stock")
    p.ylim(ymin=0)
    p.grid=True
    p.show()
    """
    
    # Stock Co-Authors
    publications = open_from_pickle("pub_stock")["documents"]
    authors = {}
    authors_value = []
    authors_name = []
    for article in publications:
        for author in article["authors"]:
            if (author["surname"] != "Stock" and author["forename"] != "Wolfgang G.") and (author["surname"] != "G. Stock" and author["forename"] != "Wolfgang"):
                name = author["forename"]+" "+author["surname"]
                if name in authors:
                    authors[name] += 1
                else:
                    authors[name] = 1
    sorted_authors = sorted(authors.iteritems(), key=operator.itemgetter(1), reverse = True)
    for element in sorted_authors:
        authors_name.append(element[0])
        authors_value.append(element[1])
    ind=range(len(authors_value))
    fig = p.figure()
    ax = fig.add_subplot(1,1,1)
    ax.bar(ind, authors_value)
    ax.set_ylabel('Anzahl gem. publizierter Artikel')
    ax.set_title("Co-Autoren von Wolfgang G. Stock")
    ax.set_xticks(ind)
    ax.set_xticklabels(authors_name)
    fig.autofmt_xdate()
    p.ylim(ymax=8)
    p.show()    
    