def main():
    with open("../data/unsorted_names.txt", "r", encoding="utf-8") as f_to_read:
        with open("../data/sorted_names.txt", "w", encoding="utf-8") as f_to_write:
            f_to_write.writelines(sorted(f_to_read))


if __name__ == "__main__":
    main()
