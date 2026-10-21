from abc import ABC, abstractmethod
from datetime import datetime, date
import csv

class InvalidLength(Exception):
    pass

class InvalidInput(Exception):
    pass

class DuplicateIds(Exception):
    pass

class InvalidDate(Exception):
    pass

class InvalidFee(Exception):
    pass

class InvalidDiscount(Exception):
    pass

class Course(ABC):
    def __init__(self, courseId, courseName, BaseFees,
                 Discount, Date, withoffer):
        self.courseId = courseId
        self.courseName = courseName
        self.BaseFees = BaseFees
        self.Discount = Discount
        self.Date = Date
        self.withoffer = withoffer

    @abstractmethod
    def calculate(self):
        pass

class ClassRoom(Course):
    def calculate(self):
        if(discount>0):
            self.withoffer=True
        return (self.BaseFees + 2000)-((self.BaseFees*self.Discount)/100)

class Online(Course):
    def calculate(self):
        if(discount>0):
            self.withoffer=True
        return self.BaseFees * 0.9-((self.BaseFees*self.Discount)/100)

courses = []
rejectedCourses = []

try:
    with open("data.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                course_id=row["CourseID"].strip()
                name=row["CourseName"].strip()
                course_type=row["CourseType"].strip()
                fees=row["BaseFee"].strip()
                discount=row["OfferDiscount"].strip()
                expdate=row["OfferEndDate"].strip()
                if not course_id:
                    raise InvalidInput("Course ID cannot be empty")
                if not name:
                    raise InvalidInput("Course name cannot be empty")
                for i in courses:
                    if(i.courseId ==course_id):
                        raise DuplicateIds(f"the course id {course_id} is duplicate")
                if course_type not in ("Classroom", "Online"):
                    raise InvalidInput("Invalid course type")
                try:
                    fees = float(fees)
                except ValueError:
                    raise InvalidFee("Base fee must be numeric")
                if fees <= 0:
                    raise InvalidFee("Base fee must be greater than zero")
                try:
                    discount = float(discount)
                except ValueError:
                    raise InvalidDiscount("Discount must be numeric")
                if not 0 <= discount <= 100:
                    raise InvalidDiscount(
                        "Discount must be between 0 and 100"
                    )
                if expdate == "":
                    offerdate = None
                else:
                    try:
                        offerdate = datetime.strptime(
                            expdate, "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        raise InvalidDate("Invalid offer end date")
                withoffer = (
                    discount > 0
                    and offerdate is not None
                    and offerdate >= date.today()
                )
                if not withoffer:
                    discount = 0

                if course_type == "Classroom":
                    obj = ClassRoom(
                        course_id, name, fees,
                        discount, offerdate, withoffer
                    )
                else:
                    obj = Online(
                        course_id, name, fees,
                        discount, offerdate, withoffer
                    )
                courses.append(obj)
            except (
                InvalidLength,
                InvalidInput,
                DuplicateIds,
                InvalidDate,
                InvalidFee,
                InvalidDiscount,
                ValueError,
                KeyError,
                AttributeError
            ) as e:
                rejectedCourses.append((row, str(e)))
                continue
            
except FileNotFoundError:
    print("Error: courses.csv was not found.")
print("Valid courses:", len(courses))
print("Rejected courses:", len(rejectedCourses))
with open("errors.txt", "w", ) as error_file:
    for row, reason in rejectedCourses:
        error_file.write(f"Record: {row}\n")
        error_file.write(f"Reason: {reason}\n\n")
with open("output.txt","w",) as file:
    for obj in courses:
        file.write(f"{obj.courseId},{obj.courseName},{obj.BaseFees},{obj.Discount},{obj.Date},{obj.withoffer},{obj.calculate()}\n")
        # courseId, courseName, BaseFees,Discount, Date, withoffer