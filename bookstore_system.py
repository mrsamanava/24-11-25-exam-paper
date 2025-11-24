
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Bookstore:

    def __init__(self,inventory_file, sales_file):
        self.inventory = pd.read_csv(inventory_file)
        self.sales = pd.read_csv(sales_file)
        self.inventory.dropna(inplace=True)
        self.sales.dropna(inplace=True)

        self.merge_data()


    def merge_data(self):
        self.data = pd.merge(self.sales, self.inventory, on="Title", how="left")
        self.data["Date"] = pd.to_datetime(self.data["Date"])

    def add_book(self, title, author, genre, price, quantity):
        new_book = {
            "Title": title,
            "Author": author,
            "Genre": genre,
            "Price": price,
            "Quantity": quantity
        }
        self.inventory = self.inventory.append(new_book, ignore_index=True)


    def update_inventory(self, title, qty):
        if title in self.inventory["Title"].values:
            self.inventory.loc[self.inventory["Title"] == title, "Quantity"] += qty


    def record_sale(self, title, qty):
        if title not in self.inventory["Title"].values:
            return

        price = self.inventory.loc[self.inventory["Title"] == title, "Price"].values[0]
        revenue = qty * price

        new_sale = {
            "Date": pd.Timestamp.today().strftime("%Y-%m-%d"),
            "Title": title,
            "Quantity Sold": qty,
            "Total Revenue": revenue
        }
        self.sales = self.sales.append(new_sale, ignore_index=True)

    def analytics(self):
        total_revenue = self.data["Total Revenue"].sum()
        best_book = self.data.groupby("Title")["Quantity Sold"].sum().idxmax()
        genre_revenue = self.data.groupby("Genre")["Total Revenue"].sum()
        print("\n---- ANALYSIS REPORT ----")
        print("Total Revenue:", total_revenue)
        print("Best Selling Book:", best_book)
        print("\nRevenue by Genre:\n", genre_revenue)

    def charts(self):
        sns.set(style="whitegrid")

        genre_rev = self.data.groupby("Genre")["Total Revenue"].sum()
        plt.figure(figsize=(8,5))
        sns.barplot(x=genre_rev.index, y=genre_rev.values)
        plt.title("Revenue by Genre")
        plt.show()


        daily = self.data.groupby("Date")["Total Revenue"].sum()
        plt.figure(figsize=(8,5))
        plt.plot(daily.index, daily.values, marker="o")
        plt.title("Daily Sales Trend")
        plt.show()

        plt.figure(figsize=(8,8))
        genre_rev.plot(kind="pie", autopct="%1.1f%%")
        plt.title("Genre Revenue Share")
        plt.show()

store = Bookstore("inventory.csv", "sales.csv")
store.analytics()
store.charts()
df = pd.read_csv("sales.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
pivot = df.pivot_table(
    values="Quantity Sold",
    index="Title",
    columns="Date",
    aggfunc="sum"
)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt="g", linewidths=.5, cmap="viridis")
plt.title("Heatmap of Book Sales by Date")
plt.xlabel("Date")
plt.ylabel("Book Title")
plt.tight_layout()
plt.show()

print("\nProject Completed Successfully!")
