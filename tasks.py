from invoke import task
import shlex

def busyboxPost(ctx, podProvider='deploy/foo', host='127.0.0.1', port=80, req='POST /-/reload'):
    echoCmd = shlex.join(['echo', '-ne', rf'{req} HTTP/1.0\n\n'])
    ncCmd = shlex.join(['nc', host, str(port)])
    pipeline = f'{echoCmd} | {ncCmd}'
    remoteCmd = shlex.join(['sh', '-c', pipeline])
    print(remoteCmd)
    ctx.run(f'''kubectl exec {podProvider} -- {remoteCmd}''')


@task
def config(ctx):
    ctx.run('kubectl delete --ignore-not-found=true configmap/prometheus-config')
    ctx.run('kubectl create configmap prometheus-config --from-file=rules.yml,prometheus.yml')
    try:
        busyboxPost(ctx, podProvider="deploy/prometheus", port=9090, req='POST /-/reload')
    except Exception:
        pass
    print('sent /-/reload but that may not have reloaded rules.yml')


@task(pre=[config])
def dev(ctx):
    ctx.run('skaffold --filename=wrapped_skaffold.yaml dev')

@task(pre=[config])
def run(ctx):
    ctx.run('skaffold --filename=wrapped_skaffold.yaml run')
