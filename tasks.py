from invoke import task
@task
def rebuild_config(ctx):
    ctx.run('/my/proj/ansible/4layer_kube/manifests/cluster_curl http://prometheus.default.svc.cluster.local/-/reload -X POST', pty=True)
