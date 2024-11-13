from controller.loader import Loader

if __name__ == '__main__':
    loader = Loader(conf_file='config/config.json')
    loader.print_indexes()
    return_map = {}
    print(loader.indexes[0].volatility)