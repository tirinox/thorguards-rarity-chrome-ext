"""
Run this script, enter ThorGuard ID (not token ID!) and see its rarity
(Don't forget to run download.py first!)
"""

from convert_metadata import load_all_meta


def main():
    all_meta = load_all_meta()
    while True:
        input_str = input('Enter ID? ')
        try:
            ident = int(input_str)
            guard = all_meta['map'][str(ident)]
            print(guard)
        except Exception as e:
            print(f'Error: {e}. Stop!')
            break


if __name__ == '__main__':
    main()
