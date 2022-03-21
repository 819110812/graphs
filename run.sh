
function run() {
    cd cmd/ && python3 main.py
}


function generate_env(){
   pip install pipreqs
   pipreqs . --force
}

function get_spacy_cn() {
    wget  https://github.com/howl-anderson/Chinese_models_for_SpaCy/releases/download/v2.2.X-0.1.0/zh_core_web_sm-0.1.0.tar.gz --no-check-certificate
}

function install() {
    pip install -r requirements.txt
    get_spacy_cn
    pip install zh_core_web_sm-0.1.0.tar.gz
    brew install libarchive
    brew install little-cms2
    brew install zstd
    brew install tesseract
}

function dev() {
    install
    docker
}

function docker() {
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.1.0
}



case  ${1:-} in
    run)
        run
        ;;
    generate_env)
        generate_env
        ;;
    get_spacy_cn)
        get_spacy_cn
        ;;
    install)
        install
        ;;
    dev)
        dev
        ;;
    *)
        echo "Usage: $0 run|generate_env|get_spacy_cn|install|dev"
        exit 1
        ;;
esac

