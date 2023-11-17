import yaml

def write_yaml(file_path, data):
    with open(file_path, 'w') as f:
        yaml.dump(data, f)

def read_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# 데이터 설정
data = {
    'train': '../data/train/',
    'val': '../data/valid/',
    'test': '../data/test/',
    'names': ['butter', 'cabbage', 'chilipepper', 'egg', 'garlic', 'greenonion', 'kimchi', 'meat', 'milk', 'mushroom', 'onion', 'potato', 'sausage', 'tofu'],
    'nc': 14
}

# YAML 파일 경로 설정
yaml_file_path = '../data/Ingre.yaml'

# YAML 파일 작성
write_yaml(yaml_file_path, data)

# YAML 파일 읽기 및 내용 출력
yaml_data = read_yaml(yaml_file_path)
print(yaml_data)
