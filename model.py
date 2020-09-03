"""
Copyright 2020, All rights reserved.
Author : SangJae Kang
Mail : craftsangjae@gmail.com
"""
from annoy import AnnoyIndex
import pandas as pd


class RepositoryModel:
    tree: AnnoyIndex
    repo2id: dict
    id2repo: dict

    def __init__(self, embed_path, num_trees=10):
        self.num_trees = num_trees
        embedding = self.load_embedding(embed_path)
        self.initialize_annoy_index(embedding)

    def load_embedding(self, embed_path):
        df: pd.DataFrame = pd.read_hdf(embed_path, "repository")

        indices = df.index.tolist()
        self.repo2id = {str(repo_id): tree_id for tree_id, repo_id in enumerate(indices)}
        self.id2repo = {tree_id: str(repo_id) for tree_id, repo_id in enumerate(indices)}

        return df.values

    def initialize_annoy_index(self, embedding):
        embedding_size = embedding.shape[1]
        self.tree = AnnoyIndex(embedding_size, "dot")

        for i, vector in enumerate(embedding):
            self.tree.add_item(i, vector)

        self.tree.build(self.num_trees)

    def query(self, repo_id, nums_to_recommend, include_score=False):
        if include_score:
            recommended_tree_ids, scores = (self.tree.get_nns_by_item(
                self.repo2id[repo_id], nums_to_recommend, include_distances=True))
            recommended_repo_ids = [self.id2repo[i] for i in recommended_tree_ids]
            return recommended_repo_ids, scores
        else:
            recommended_tree_ids = (self.tree.get_nns_by_item(
                self.repo2id[repo_id], nums_to_recommend, include_distances=False))
            recommended_repo_ids = [self.id2repo[i] for i in recommended_tree_ids]
            return recommended_repo_ids

    def can_query(self, repo_id):
        try:
            return str(repo_id) in self.repo2id
        except:
            return False







