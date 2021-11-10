

class Quark:
    """ An :class:`src.ops.ElementalOperator` is a product of quark fields and
        other commuting objects.
        :param barred: Specifies if quark or anti-quark
        :type barred: bool
        :param flavor: Quark flavor
        :type flavor: char
        :param spin: Quark spin
        :type spin: str
        :param color: Quark color
        :type color: str
        :param time: Quark time
        :type time: str
        :param position: Quark position
        :type position: str
    """
    def __init__(self, barred, flavor, spin, color, time, position):
        """Constructor
        """
        self.barred=barred
        self.flavor=flavor
        self.spin=spin
        self.color=color
        self.time=time
        self.position=position

    def __str__(self):
        """Printer to string
        """
        if self.barred:
            return "\\bar{" + str(self.flavor) + "}" + "_{" + self.spin + " " \
                   +  self.color + "}(" + self.position + ", " + self.time + ")"
        else:
            return str(self.flavor) + "_{" + self.spin + " " +  self.color \
                   + "}(" + self.position + ", " + self.time + ")"

    def __eq__(self, other):
        """Check if two quarks are equal
            :param other: Another quark
            :type other: :class:`src.ops.Quark`
        """
        return (self.barred==other.barred) and (self.flavor==other.flavor) and \
               (self.spin==other.spin) and (self.color==other.color) and       \
               (self.time==other.time) and (self.position==other.position)


#TODO Implement this for the wick_contraction part. 
class ShortQuark:
    """ A more efficient implementation of :class:`src.ops.Quark` for use
        within LINK_TO_WICK_CONTRACTION.
        :param barred: Quark or anti-quark
        :type barred: bool
        :param flavor: Quark flavor
        :type flavor: char
        :param label: Single label for the quark
        :type lavel: str
    """

    def __init__(self, barred, flavor, label):
        """Constructor
        """
        self.barred=barred
        self.flavor=flavor
        self.label=label

    def __str__(self):
        """Printer to string
        """
        if(self.barred):
            return "\\bar{" + str(self.flavor) + "}_{" + self.label + "}"
        else:
            return str(self.flavor) + "_{" + self.label + "}"

    def __eq__(self, other):
        """Check if two short quarks are equal
            :param other: Another short quark
            :type other: :class:`src.ops.ShortQuark`
        """
        return (self.barred==other.barred) and (self.flavor==other.flavor)     \
               and (self.label==other.label)
