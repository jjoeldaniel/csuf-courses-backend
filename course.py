class Course:
    def __init__(
        self, name: str, description: str, prereqs: str | None, coreqs: str | None
    ) -> None:
        self.name = name
        self.description = description
        self.prereqs = prereqs
        self.coreqs = coreqs

    def __repr__(self) -> str:
        return str(
            {
                "name": self.name,
                "description": self.description,
                "prereqs": self.prereqs,
                "coreqs": self.coreqs,
            }
        )

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n\n"
            f"Description: {self.description}\n\n"
            f"Prerequisites: {self.prereqs}\n"
            f"Corequisites: {self.coreqs}"
        )
