import csv

data = (
    ('1', '2019-01-01', '4343', 'Brand 1', '1234'),
    ('2', '2019-06-04', '1432', 'Brand 2', '2345'),
    ('3', '2019-06-06', '4343', 'Brand 3', '9876'),
    ('4', '2020-02-08', '1232', 'Brand 2', '8765'),
    ('5', '2020-04-25', '7789', 'Brand 4', '7645'),
    ('6', '2020-07-14', '7789', 'Brand 1', '2345'),
    ('7', '2020-06-18', '1232', 'Brand 1', '2345'),
    ('8', '2021-04-17', '1432', 'Brand 2', '9876')
)
with open('api/data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Id", "Timestamp", "Asin", "Brand", "CustomerId"])
    for i in data:
        writer.writerow(i)
