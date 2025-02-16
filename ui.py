
# Dat Nguyen
# dattn10@uci.edu
# 46759936


import Profile
import os

profile = None


# Function to process user commands
def process_command(command: str):
    global profile, file_path
    parts = command.split()
    if not parts:
        print("Invalid command.")
        return

    cmd = parts[0].upper()

    if cmd == "C":  # creates profile/file in directory
        try:
            # ensures no empty names
            if "-n" not in parts or parts.index("-n") + 1 >= len(parts):
                print("Error: Need journal name")
                return

            path_index = parts.index("-n") - 1
            path = parts[path_index]
            name = parts[path_index + 2]

            if not path or not name:
                print("Error: Missing path or name")
                return

            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            bio = input("Enter a bio: ").strip()

            if not username or not password:
                print("Error: Username and password cannot be empty.")
                return

            # gives user output of what they chose
            file_path = os.path.join(path, f"{name}.dsu")
            print(f"Path entered: {path}")
            print(f"Journal name: {name}")

            print(f"Creating new journal: {file_path}")
            profile = Profile.Profile(
                dsuserver="", username=username, password=password
            )
            profile.bio = bio
            profile.save_profile(file_path)
            print(f"Profile saved at {file_path}")

        except Exception as e:
            print(f"Error creating profile: {e}")
            return

    elif cmd == "O":  # open profile
        try:
            file_path = parts[1]
            profile = Profile.Profile()
            profile.load_profile(file_path)
            print(f"Profile loaded from {file_path}")
        except Exception as e:
            print(f"Error loading profile: {e}")

    elif cmd == "E":  # edit profile
        if profile is None:
            print("Error: No profile exists")
            return
        try:
            post_ids = []
            # captures index and command
            for i, part in enumerate(parts):
                # ensures if usr or bio > 1 captures all
                if part == "-usr":
                    if i + 1 < len(parts):
                        username_parts = []
                        j = i + 1
                        while j < len(parts) and not parts[j].startswith('-'):
                            username_parts.append(parts[j])
                            j += 1
                        profile.username = " ".join(username_parts)
                        print(f"Username chosen is {profile.username}")
                    else:
                        print("Error: Missing username.")
                        return

                elif part == "-pwd":  # captures password; ensures content
                    if i + 1 < len(parts):
                        profile.password = parts[i + 1]
                    else:
                        print("Error: Missing password.")
                        return

                elif part == "-bio":  # captures bio; ensures there is content
                    if i + 1 < len(parts):
                        bio_parts = []
                        j = i + 1
                        while j < len(parts) and not parts[j].startswith('-'):
                            bio_parts.append(parts[j])
                            j += 1
                        profile.bio = " ".join(bio_parts)
                    else:
                        print("Error: Missing bio")
                        return
                # captures post; ensures content
                elif part == "-addpost":
                    if i + 1 < len(parts):
                        post_parts = []
                        j = i + 1
                        # captures only up till next command
                        while j < len(parts) and not parts[j].startswith('-'):
                            post_parts.append(parts[j])
                            j += 1
                        profile.add_post(Profile.Post(" ".join(post_parts)))
                        i = j - 1
                    # No blank entries
                    else:
                        print("Error: No post content")
                        return

                elif part == "-delpost" and i + 1 < len(parts):
                    j = i + 1
                    while j < len(parts) and parts[j].isdigit():
                        # collect delete indices
                        post_ids.append(int(parts[j]))
                        j += 1
                    i = j - 1

            # process deletion AFTER loop
            # remove duplicates & sort numerically descending
            post_ids = sorted(set(post_ids), reverse=True)
            posts = profile.get_posts()

            for post_value in post_ids:
                if 0 <= post_value < len(posts):
                    profile.del_post(post_value)
                    print(f"Post {post_value} deleted")
                else:
                    print(f"Error: Post {post_value} doesn't exist")

            # save profile data after loop
            profile.save_profile(file_path)
            print("Profile updated.")

        except Exception as e:
            print(f"Error editing profile: {e}")

    elif cmd == "P":  # print profile data
        if profile is None:
            print("Error: No profile exists")
            return
        try:
            if "-all" in parts:
                print(f"Username: {profile.username}")
                print(f"Password: {profile.password}")
                print(f"Bio: {profile.bio}")
                print("Posts:")
                for idx, post in enumerate(profile.get_posts()):
                    print(f"Post {idx}: {post.entry}")

            elif "-usr" in parts:
                print(f"Username: {profile.username}")

            elif "-pwd" in parts:
                print(f"Password: {profile.password}")

            elif "-bio" in parts:
                print(f"Bio: {profile.bio}")

            elif "-posts" in parts:
                for idx, post in enumerate(profile.get_posts()):
                    print(f"Post {idx}: {post.entry}")

            elif "-post" in parts:
                index = parts.index("-post") + 1
                if index < len(parts):
                    try:
                        post_id = int(parts[index])
                        posts = profile.get_posts()
                        if 0 <= post_id < len(posts):
                            print(f"Post {post_id}: {posts[post_id].entry}")
                        else:
                            print("Error: Invalid post ID.")
                    except ValueError:
                        print("Error: Post ID must be an integer.")
                else:
                    print("Error: Missing post ID.")
            else:
                print("Invalid print option.")
        except Exception as e:
            print(f"Error reading profile: {e}")
    else:
        print("Unknown command.")
