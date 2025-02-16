from pathlib import Path
import ui


def main():
    print("Welcome to the Journal Program")

    mode = input(
        "Enter 'admin' for Admin Mode or press Enter for User-Friendly Mode: "
    ).strip().lower()

    # Allows user to choose between admin or user mode
    if mode == "admin":
        print("Entering Admin Mode. Type commands as per the format.")
        while True:
            command = input("> ").strip()
            if command.lower() in ["exit", "quit"]:
                print("Exiting Admin Mode")
                break
            ui.process_command(command)
    else:
        user_friendly_interface()


def user_friendly_interface():
    while True:
        print("\nOptions:\n[C] Create Journal\n[O] Open Journal"
              "\n[E] Edit Journal\n[P] Print Journal\n[Q] Quit")
        choice = input("Select an option: ").strip().lower()

        # creates a 'profile' within a directory
        if choice == 'c':
            path = input("Enter directory path: ").strip()
            d_path = Path(path)

            # checks if the directory exists
            if not d_path.exists() or not d_path.is_dir():
                print("Directory doesn't exist, try again")
                continue

            while True:
                name = input("Enter journal name: ").strip()
                if not name:
                    print("Must have valid name")
                    continue
                break

            f_path = d_path / f"{name}.dsu"

            # creates a .dsu file within the directory, and checks if it exists
            if f_path.exists():
                print("File already exists, loading journal")
                ui.process_command(f"O {f_path}")
                return

            # creates and confirms creation of file
            f_path.touch()
            print(f"{f_path} created")
            ui.process_command(f"C {path} -n {name}")

        # opens a file to use for edit and print options
        elif choice == 'o':
            file_path = input("Enter full file path to open (.dsu): ").strip()
            ui.process_command(f"O {file_path}")

        # allows user to edit with the 'E' command
        elif choice == 'e':
            edit_options = input(
                "Enter edit options\n"
                " -usr [USERNAME]\n -pwd [PASSWORD]\n -bio [BIO]\n"
                " -addpost [NEW POST]\n -delpost [ID]\n"
            ).strip()
            ui.process_command(f"E {edit_options}")

        # reads/prints contents of the profile
        elif choice == 'p':
            print_options = input(
                "Enter print options (-all, -usr, -posts): "
            ).strip()
            ui.process_command(f"P {print_options}")

        # quits the program
        elif choice == 'q':
            print("Exiting journal program")
            break

        else:
            print("Invalid option : Try again")


if __name__ == "__main__":
    main()
