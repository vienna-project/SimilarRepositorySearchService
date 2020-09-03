"""
Copyright 2020, All rights reserved.
Author : SangJae Kang
Mail : craftsangjae@gmail.com
"""
from sanic import Sanic
from sanic import response as res
from sanic import request as req
from model import RepositoryModel
from config import Setting

app = Sanic("SimilarRepositorySearchService")
app.config.from_object(Setting)

repository_model: RepositoryModel = None


@app.route('/repository', methods=["GET", "POST"])
async def search_similar_repository(request: req):
    """ <repo_id>와 유사한 <nums>개의 repository를 가져오기
    """
    repo_id = request.args.get('repo_id', "")

    if not repo_id:
        return res.text("argument:<repo_id> is required", status=400)

    if not repository_model.can_query(repo_id):
        return res.text(f"Sorry... repo({repo_id}) is not included in the recommended list", status=404)

    nums = request.args.get("nums", "10")
    if not nums.isnumeric():
        return res.text(f"nums should be numeric and upper than 0", status=400)
    else:
        nums = int(nums)

    include_scores = bool(request.args.get("include_scores", None))

    if include_scores:
        reco_repo_ids, reco_scores = repository_model.query(repo_id, nums, include_scores)
        return res.json({"repos": reco_repo_ids, "scores": reco_scores})
    else:
        reco_repo_ids = repository_model.query(repo_id, nums, include_scores)
        return res.json({"repos": reco_repo_ids})


@app.listener("before_server_start")
async def setup_reco_model(app: Sanic, loop):
    """ Server가 Launch되기 전, recommendation Model을 불러오기
    """
    global repository_model
    repository_model = RepositoryModel(app.config['EMBED_PATH'], app.config['NUM_TREES'])


if __name__ == "__main__":
    """
    Gunicorn : WSGI
    
    For Deployment:
    gunicorn server:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
    """
    app.run(host='0.0.0.0', port=8000)
