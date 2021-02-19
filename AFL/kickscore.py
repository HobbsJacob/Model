import kickscore as ks
import csv


model = ks.BinaryModel()

gc = ks.kernel.Constant(var=1.0) + ks.kernel.Matern52(var=0.5, lscale=1.0)
bl = ks.kernel.Exponential(var=1, lscale=1)
r = ks.kernel.Exponential(var=1, lscale=1)
c = ks.kernel.Exponential(var=1, lscale=1)
wce = ks.kernel.Exponential(var=1, lscale=1)
gg = ks.kernel.Exponential(var=1, lscale=1)
wb = ks.kernel.Exponential(var=1, lscale=1)
e = ks.kernel.Exponential(var=1, lscale=1)
h = ks.kernel.Exponential(var=1, lscale=1)
pa = ks.kernel.Exponential(var=1, lscale=1)
av = ks.kernel.Exponential(var=1, lscale=1)
nm = ks.kernel.Exponential(var=1, lscale=1)
f = ks.kernel.Exponential(var=1, lscale=1)
sk = ks.kernel.Exponential(var=1, lscale=1)
ca = ks.kernel.Exponential(var=1, lscale=1)
ss = ks.kernel.Exponential(var=1, lscale=1)
m = ks.kernel.Exponential(var=1, lscale=1)
gcs = ks.kernel.Exponential(var=1, lscale=1)

model.add_item("Geelong Cats", kernel=gc)
model.add_item( "Brisbane Lions", kernel=gc)
model.add_item("Richmond" , kernel=gc)
model.add_item("Collingwood" , kernel=gc)
model.add_item("West Coast Eagles" , kernel=gc)
model.add_item("GWS Giants" , kernel=gc)
model.add_item("Western Bulldogs" , kernel=gc)
model.add_item("Essendon" , kernel=gc)
model.add_item( "Hawthorn", kernel=gc)
model.add_item("Port Adelaide" , kernel=gc)
model.add_item("Adelaide Crows" , kernel=gc)
model.add_item("North Melbourne" , kernel=gc)
model.add_item("Fremantle" , kernel=gc)
model.add_item("St Kilda" , kernel=gc)
model.add_item("Carlton" , kernel=gc)
model.add_item("Sydney Swans" , kernel=gc)
model.add_item("Melbourne" , kernel=gc)
model.add_item("Gold Coast Suns" , kernel=gc)

with open("parsed.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["result"])