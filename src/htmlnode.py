class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html")

    def props_to_html(self):
        if not self.props:
            return ""

        return "".join(
            f' {key}="{value}"'
            for key, value in self.props.items()
        )

    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props}"
            f")"
        )