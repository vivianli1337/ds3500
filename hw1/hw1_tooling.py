"""
Vivian Li
DS 3500 Advanced Programming
Prof. Rachlin
01/19/2024

1) Khoury enterprise git server username: liviv623
2) Your anaconda version: conda 23.7.4
3) Your installed git version number: git version 2.39.3 (Apple Git-145)
4) Your PyCharm screenshot showing your plot and your status bar. --> see below
5) The text of the inspiring quote.
    from the secret message: “Without data, you’re just another person with an opinion.”
             W. Edwards Deming


"""""
import matplotlib.pyplot as plt
x = [1,2,3,4,5,6,7]
y = [2,4,6,8,10,12,14]
plt.bar(x,y, 0.5, align="center", color="skyblue" )
plt.title("Experimental graph - hw1")
plt.xlabel("Days of the Week")
plt.ylabel("Random data")
plt.show()

