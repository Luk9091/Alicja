import dwfpy as dwf


class Analyzer():
    def __init__(self):
        self.dev = dwf.Device(0)

    def __del__(self):
        self.dev.close()


    @property
    def name(self) -> str | None:
        return self.dev.name



if __name__ == "__main__":
    analyzer = Analyzer()
    print(f"Analyzer name: {analyzer.name}")