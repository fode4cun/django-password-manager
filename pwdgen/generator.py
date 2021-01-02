from dataclasses import dataclass
from random import choice, sample
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

CHARS = {
    'lowercase': ascii_lowercase,
    'uppercase': ascii_uppercase,
    'numbers': digits,
    'punctuation': punctuation
}


@dataclass
class Generator:
    data: dict

    def gen(self) -> str:
        password = ''
        keys = list(set(CHARS) & set(self.data))

        if keys:
            for i in range(int(self.data['length_range'])):
                key = keys[i % len(keys)]
                password += choice(CHARS[key])

            password = ''.join(sample(password, len(password)))

        return password
