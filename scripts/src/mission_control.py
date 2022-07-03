import argparse as ag


def run (path_partitura, path_instrumento):
    print(path_instrumento, path_partitura)

if __name__ == '__main__':
    parser = ag.ArgumentParser(description= "Implementation of sounds in the metallophone")
    parser.add_argument("p", help = "The path to the music sheet")
    parser.add_argument("f", help = 'Frecuency')
    parser.add_argument('i', help = 'instrument')
    parser.add_argument('o', help = 'audio in wave format')

    args = parser.parse_args()
    run (args.p, args.i)


#para correrlo en la terminal copiar path del archivo


