import numpy as np
import pathsim
import utils
import time
import ppagerank

(
    author_info,
    paper_info,
    venue_info,
    num_author_map,
    num_paper_map,
    num_venue_map,
    paper_author_adj,
    paper_venue_adj,
) = utils.load_data()
k = 10  # 要找的相似作者的数量 -- (EN: Number of similar authors to find)
AP_author = 222  # 作者编号 -- (EN: Author number)
VPA_venue = 19


def make_AP_adj():
    """
    处理AP类型的关系矩阵Ml
    :return: Ml，APA关系矩阵的对角线元素

    En:
    Processing the relationship matrix Ml of type AP
    :return: Ml, the diagonal elements of the APA relationship matrix
    """
    AP_adj = np.mat(paper_author_adj).T
    diag = []
    for i in range(len(AP_adj)):
        mii = np.mat(AP_adj[i]) * np.mat(AP_adj[i].T)
        diag.append(mii)
    return AP_adj, diag


def make_APV_adj():
    """
    处理APV类型的关系矩阵Ml
    :return: Ml，APVPA关系矩阵的对角线元素

    En:
    Processing the relationship matrix Ml of type APV
    :return: Ml, the diagonal elements of the APVPA relationship matrix
    """
    APV_adj = np.mat(paper_author_adj).T * np.mat(paper_venue_adj)
    diag = []
    for i in range(len(APV_adj)):
        mii = np.mat(APV_adj[i]) * np.mat(APV_adj[i].T)
        diag.append(mii)
    return APV_adj, diag


def make_APVPA_adj():
    """
    处理APV类型的关系矩阵Ml
    :return: Ml，APVPA关系矩阵的对角线元素

    En:
    Processing the relationship matrix Ml of type APV
    :return: Ml, the diagonal elements of the APVPA relationship matrix
    """
    APV_adj = np.mat(paper_author_adj).T * np.mat(paper_venue_adj)
    APVPA_adj = np.mat(APV_adj) * np.mat(APV_adj).T
    diag = []
    for i in range(len(APVPA_adj)):
        mii = np.mat(APVPA_adj[i]) * np.mat(APVPA_adj[i].T)
        diag.append(mii)
    return APVPA_adj, diag


def make_VPA_adj():
    """
    处理VPA类型的关系矩阵Ml
    :return: Ml，VPAPV关系矩阵的对角线元素

    En:
    Processing the relationship matrix Ml of type VPA
    :return: Ml, the diagonal elements of the VPAPV relationship matrix
    """
    VPA_adj = np.mat(paper_venue_adj).T * np.mat(paper_author_adj)
    diag = []
    for i in range(len(VPA_adj)):
        mii = np.mat(VPA_adj[i]) * np.mat(VPA_adj[i].T)
        diag.append(mii)
    return VPA_adj, diag


def make_VPAPV_adj():
    """
    处理VPA类型的关系矩阵Ml
    :return: Ml，VPAPV关系矩阵的对角线元素

    En:
    Processing the relationship matrix Ml of type VPA
    :return: Ml, the diagonal elements of the VPAPV relationship matrix

    """
    VPA_adj = np.mat(paper_venue_adj).T * np.mat(paper_author_adj)
    VPAPA_adj = np.mat(VPA_adj) * np.mat(VPA_adj).T
    diag = []
    for i in range(len(VPAPA_adj)):
        mii = np.mat(VPAPA_adj[i]) * np.mat(VPAPA_adj[i].T)
        diag.append(mii)
    return VPAPA_adj, diag


def main():
    """
    所有实验所需的操作
    有效性检验，对比APA语义下pathsim和personalized pagerank的不同结果
    元路径为APA时的语义为共同发表论文，因此验证实验效果时需统计查询到的作者与原作者共同发表论文情况

    En:
    All operations required for the experiment
    Effectiveness verification, comparison of different results of pathsim and personalized pagerank under APA semantics
    When the meta-path is APA, the semantics is co-published papers, so when verifying the experimental effect, it is necessary to
    count the situation where the queried author and the original author co-publish papers.

    """
    AP_adj, diag = (
        make_AP_adj()
    )  # 基于元路径APA的查询 -- (EN: Query based on meta-path APA)
    print("APA using pathsim:")

    start = time.time()

    model = pathsim.PathSim(np.array(AP_adj), diag)
    topk = model.baseline(
        AP_author, k
    )  # pathsim-baseline算法 -- (EN: pathsim-baseline algorithm)

    t = time.time() - start

    print("time:" + str(t))
    print("author name:")
    print(author_info[num_author_map[str(AP_author)]]["name"])
    print("paper list")
    paper = list(
        np.array(AP_adj)[AP_author].nonzero()[0]
    )  # 原作者发表的论文 -- (EN: Papers published by the original author)
    print(paper)
    print("topk：")
    for i in topk:
        print("author name:")
        print(author_info[num_author_map[str(i)]]["name"])
        print("paper list:")
        papers = list(
            np.array(AP_adj)[i].nonzero()[0]
        )  # 查到的作者发表的论文 -- (EN: Papers published by the queried author)
        print(papers)
        print("co-author paper list:")
        inter = list(
            set(paper).intersection(set(papers))
        )  # 共同发表的论文列表 -- (EN: List of co-published papers)
        print(inter)
        print("co-author paper number:")
        print(len(inter))  # 共同发表的论文篇目 -- (EN: Number of co-published papers)
    m = np.mat(AP_adj) * np.mat(AP_adj).T
    model = ppagerank.PPageRank(np.array(m), 0.9)
    print("APA using pagerank:")
    topk = model.find_topk(AP_author, k)
    print("author name:")
    print(author_info[num_author_map[str(AP_author)]]["name"])
    print("paper list")
    paper = list(
        np.array(AP_adj)[AP_author].nonzero()[0]
    )  # 原作者发表的论文 -- (EN: Papers published by the original author)
    print(paper)
    print("topk：")
    for i in topk:
        print("author name:")
        print(author_info[num_author_map[str(i)]]["name"])
        print("paper list:")
        papers = list(
            np.array(AP_adj)[i].nonzero()[0]
        )  # 查到的作者发表的论文 -- (EN: Papers published by the queried author)
        print(papers)
        print("co-author paper list:")
        inter = list(
            set(paper).intersection(set(papers))
        )  # 共同发表的论文列表   -- (EN: List of co-published papers)
        print(inter)
        print("co-author paper number:")
        print(len(inter))  # 共同发表的论文篇目 -- (EN: Number of co-published papers)

    """
    在不同语义下，pathsim有不同结果的检验，用APVPA的语义结果与APA对比
    
    En:
    In different semantics, pathsim has different results. The semantics result of APVPA is compared with APA
    """
    APV_adj, APV_diag = make_APV_adj()
    model = pathsim.PathSim(np.array(APV_adj), APV_diag)
    print("APVPA using pathsim")
    topk = model.baseline(AP_author, k)
    print("topk：")
    for i in topk:
        print(author_info[num_author_map[str(i)]]["name"])
    """
    剪枝算法的验证
    """
    APVPA_adj, APVPA_diag = make_APVPA_adj()
    model = pathsim.PathSim(np.array(APVPA_adj), APVPA_diag, dense=True)
    print("APVPAPVPA using pathsim:")

    start = time.time()

    topk = model.baseline(AP_author, k)
    t = time.time() - start

    print("baseline time:")
    print(t)

    start = time.time()

    model.pruning_init()

    t = time.time() - start
    print("pruning init time:")
    print(t)
    topk = model.pruning(AP_author, k)

    t = time.time() - start

    print("pruning search time:")
    print(t)


if __name__ == "__main__":
    main()
