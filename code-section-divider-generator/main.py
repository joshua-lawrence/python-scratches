import subprocess
from abc import ABC, abstractmethod


class Divider(ABC):
    def __init__(self, decorator, content, height, line_length):
        self.decorator = decorator
        self.content = content
        self.height = height
        self.line_length = line_length

    @abstractmethod
    def create_divider(self):
        pass

    def copy_to_clipboard(self):
        divider = self.create_divider()
        subprocess.run("pbcopy", input=divider, check=True, encoding="utf-8")
        print(f"Copied to clipboard:\n{divider}\n")


class OutlineBoxDivider(Divider):
    def __init__(self, decorator, content, height, line_length):
        super().__init__(decorator, content, height, line_length)
        self.height = height

    def create_divider(self):
        if self.line_length < 10:
            raise ValueError("Line length must be at least 10")

        words = self.content.split()
        lines = []
        current_line = ""
        for word in words:
            if (
                    len(current_line) + len(word) + 1 > self.line_length - 5
            ):
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " "
                current_line += word
        lines.append(current_line)

        border = "# " + (self.decorator * (self.line_length - 2))

        box_lines = [border]
        for line in lines:
            padded_line = f"# {self.decorator} {line.center(self.line_length - 6)} {self.decorator}"
            box_lines.append(padded_line)
        box_lines.append(border)

        return "\n".join(box_lines)


class SolidBoxDivider(Divider):
    def create_divider(self):
        if self.height < 1:
            raise ValueError("Height must be at least 1")

        content_length = len(self.content)
        if content_length > self.line_length - 4:
            raise ValueError("Text is too long for the specified width")

        even = content_length % 2 == 0

        side_length = (self.line_length - content_length - 4 if even else 5) // 2
        centered_text = f"# {self.decorator * side_length} {self.content} {self.decorator * side_length}"

        full_divider = [f"# {self.decorator * (self.line_length - 2)}" for _ in range(self.height)]
        full_divider[self.height // 2] = centered_text

        return "\n".join(full_divider)


def main():
    print("1. Solid box with specified height\n2. Outlined box with height 3")
    choice = int(input("Enter choice: "))
    content = input("Enter text to be centered in your divider: ") or ""
    decorator = input("Enter decorator (enter for ·): ") or "·"
    line_length = input("Enter line length (enter for 120): ") or 120
    if choice == 1:
        height = int(input("Enter height (enter for 3): ") or 3)
        divider = SolidBoxDivider(decorator, content, height, line_length)
    else:
        divider = OutlineBoxDivider(decorator, content, 3, line_length)
    divider.copy_to_clipboard()
    while True:
        content = input("Enter another value to run again, 'r' to restart, or enter 'q' to quit: ")
        if content == "q":
            break
        elif content == "r":
            main()
            break
        else:
            divider.content = content
            divider.copy_to_clipboard()


if __name__ == "__main__":
    main()


