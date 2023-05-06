import pyautogui as pag
import random as rd
from pyclick import HumanCurve
import pytweening
import numpy as np
import time

pag.MINIMUM_SLEEP = 0.01  # Default: 0.05


class FakeAction(object):
    def __init__(self) -> None:
        pass

    def scrollDownBy(self, height):
        step = int(height / 200)
        for i in range(step//2):
            pag.scroll(-200)
        time.sleep(0.3)
        for i in range(step//2):
            pag.scroll(-200)

    def scrollUpBy(self, height):
        step = int(height / 200)
        for i in range(step//2):
            pag.scroll(200)
        time.sleep(0.4)
        for i in range(step//2):
            pag.scroll(200)

    def moveTo(self, x, y, **kwargs):
        # sourcery skip: use-contextlib-suppress
        """
        Use Bezier curve to simulate human-like mouse movements.
        Args:
            destination: x, y tuple of the destination point
            destination_variance: pixel variance to add to the destination point (default 0)
        Kwargs:
            knotsCount: number of knots to use in the curve, higher value = more erratic movements
                        (default determined by distance)
            mouseSpeed: speed of the mouse (options: 'slowest', 'slow', 'medium', 'fast', 'fastest')
                        (default 'slow')
            tween: tweening function to use (default easeInOutQuad)
        """
        offsetBoundaryX = kwargs.get("offsetBoundaryX", 100)
        offsetBoundaryY = kwargs.get("offsetBoundaryY", 100)
        knotsCount = kwargs.get(
            "knotsCount", FakeAction.__calculate_knots(x, y))
        distortionMean = kwargs.get("distortionMean", 1)
        distortionStdev = kwargs.get("distortionStdev", 1)
        distortionFrequency = kwargs.get("distortionFrequency", 0.5)
        tween = kwargs.get("tweening", pytweening.easeInOutQuad)
        mouseSpeed = kwargs.get("mouseSpeed", "slow")
        mouseSpeed = FakeAction.__get_mouse_speed(mouseSpeed)

        dest_x = x
        dest_y = y

        start_x, start_y = pag.position()
        for curve_x, curve_y in HumanCurve(
            (start_x, start_y),
            (dest_x, dest_y),
            offsetBoundaryX=offsetBoundaryX,
            offsetBoundaryY=offsetBoundaryY,
            knotsCount=knotsCount,
            distortionMean=distortionMean,
            distortionStdev=distortionStdev,
            distortionFrequency=distortionFrequency,
            tween=tween,
            targetPoints=mouseSpeed,
        ).points:
            pag.moveTo((curve_x, curve_y))
            start_x, start_y = curve_x, curve_y

    def moveRel(self, x: int, y: int, x_var: int = 0, y_var: int = 0, **kwargs):
        """
        Use Bezier curve to simulate human-like relative mouse movements.
        Args:
            x: x distance to move
            y: y distance to move
            x_var: random upper-bound pixel variance to add to the x distance (default 0)
            y_var: random upper-bound pixel variance to add to the y distance (default 0)
        Kwargs:
            knotsCount: if right-click menus are being cancelled due to erratic mouse movements,
                        try setting this value to 0.
        """
        if x_var != 0:
            x += np.random.randint(-x_var, x_var)
        if y_var != 0:
            y += np.random.randint(-y_var, y_var)
        self.move_to((pag.position()[0] + x, pag.position()[1] + y), **kwargs)

    def __calculate_knots(x, y):
        """
        Calculate the knots to use in the Bezier curve based on distance.
        Args:
            destination: x, y tuple of the destination point
        """
        # calculate the distance between the start and end points
        distance = np.sqrt((x - pag.position()[0])
                           ** 2 + (y - pag.position()[1]) ** 2)
        res = round(distance / 200)
        return min(res, 3)

    def __get_mouse_speed(speed: str) -> int:
        """
        Converts a text speed to a numeric speed for HumanCurve (targetPoints).
        """
        if speed == "slowest":
            return rd.randint(85, 100)
        elif speed == "slow":
            return rd.randint(65, 80)
        elif speed == "medium":
            return rd.randint(45, 60)
        elif speed == "fast":
            return rd.randint(20, 40)
        elif speed == "fastest":
            return rd.randint(10, 15)
        else:
            raise ValueError(
                "Invalid mouse speed. Try 'slowest', 'slow', 'medium', 'fast', or 'fastest'.")

    def randomMove(self, x_range: tuple, y_range: tuple, x_des: int, y_des: int, **kwargs):
        """
        Random move in a rectangle area, and the move mouse to the destination
        **Args:
            x_range, y_range: tuple (x1,x2), (y1,y2)
            x_des, y_des: int 
        **Kwargs
            mouseSpeed: speed of the mouse (options: 'slowest', 'slow', 'medium', 'fast', 'fastest')
                        (default 'medium')
            duration: Duration in seconds for random move in the rectangle area (default 1)
        """
        # Get information from **Kwargs
        mouseSpeed = kwargs.get("mouseSpeed", "medium")
        mouseSpeed = FakeAction.__get_mouse_speed(mouseSpeed)
        duration = kwargs.get("duration", 1)

        # Call the super class()
        mouse = FakeAction()

        # Random move in specific timing
        start_time = time.time()
        while (time.time() - start_time < duration):
            time.sleep(0.05)
            mouse.moveTo(
                x=rd.randint(x_range[0], x_range[1]),
                y=rd.randint(y_range[0], y_range[1]),
                mouseSpeed='medium',
                knotsCount=5,
                destination_variance=200)

        # Move to the destination point
        time.sleep(0.1)
        mouse.moveTo(
            x=x_des,
            y=y_des,
            mouseSpeed='medium',
            knotsCount=5,
            destination_variance=100)

    def fakeTyping(self, content: str, **kwargs):
        """
        Simulate Human typing with typos
        Args: 
            content: Your string (str)
        Kwargs: 
            numTypos: The number of times (int) you type the infomation wrong (must be less than the length of content) (default 1)
        """
        # Get info from kwargs
        length = len(content)
        numTypos = kwargs.get('numTypos', 1)

        if numTypos == 0:
            pag.write(content, interval=rd.uniform(0.05, 0.15))
            time.sleep(rd.uniform(0.05, 0.15))
            return
        elif numTypos >= length:
            raise ValueError(
                "The number of times (int) you type the infomation wrong (must be less than the length of content)")

        time.sleep(rd.uniform(0.15, 0.3))

        # Choose position to perform typos except the first letter
        lst = [i for i in range(length) if i != 0]
        position_of_typos = rd.sample(lst, k=numTypos)
        position_of_typos.sort()

        # Slice the content
        """
            For example, my content is: "sales@hotmail.com"
            positions = [3,6,7]
            Then I will try to slice this string into 4 part whose indexes are in range:: (0,3); (3,6); (6,7); (7,16)
        """
        slicers = []

        for i, x in enumerate(position_of_typos):
            if numTypos == 1:
                slicers.append([0, x-1])
                slicers.append([x, length-1])
            else:
                if i == 0:
                    slicers.append([0, x-1])
                elif i == numTypos - 1:
                    slicers.append([position_of_typos[i-1], x-1])
                    slicers.append([x, length-1])
                else:
                    slicers.append([position_of_typos[i-1], x-1])

        # List of sliced words
        sliced_words = [content[x[0]:x[1]+1] for x in slicers]

        # Generate list of typo words of length defined in list
        typos = [rd.randint(1, 4) for i in range(len(position_of_typos))]
        typo_words = []
        for x in typos:
            letters = [chr(rd.randint(ord('a'), ord('z'))) for i in range(x)]
            typo_words.append(''.join(letters))

        # Start type
        for i, word in enumerate(sliced_words):
            pag.write(word, interval=rd.uniform(0.05, 0.2))
            if i < numTypos:
                pag.write(typo_words[i], interval=rd.uniform(
                    0.05, 0.2))  # Type wrong
                time.sleep(rd.uniform(0.05, 1))
                pag.press('backspace', presses=len(
                    typo_words[i]), interval=rd.uniform(0.05, 0.2))  # Delete wrong letters
                time.sleep(rd.uniform(0.05, 0.2))
