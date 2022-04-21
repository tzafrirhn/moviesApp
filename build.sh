app_image=movies_app_img
app_container=movies_app_con
app_network=movies_app_internal
mongo_image=mongo
mongo_container=movies_app_mongo

_build()
{
  . venv/bin/activate
  rm -rf src/__pycache__ &>/dev/null
  docker rmi -f "$app_image:latest"
  docker build -t "$app_image" -f Dockerfile .
}

_run()
{
  docker network create "$app_network" || :
  docker run "--net=$app_network" --detach --rm "--hostname=$mongo_container" "--name=$mongo_container" --expose 27017 mongo
  docker run "--net=$app_network" --rm -e "PROJ_MONGO_HOST=$mongo_container" "--name=$app_container" -p 80:5000   \
    --env-file docker_env "$app_image"
}

_kill()
{
  docker kill "$mongo_container"
  docker kill "$app_container"
  docker network rm "$app_network" || :
}

(( $# )) || set -- build
while (( $# )); do
  case $1 in
    build) _build ;;
    run)   _run   ;;
    kill)  _kill  ;;
  esac ; shift
done
