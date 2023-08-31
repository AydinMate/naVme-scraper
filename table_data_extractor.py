class TableDataExtractor:
    def __init__(self, page):
        self.page = page

    async def extract_table_data(self):
        # Find the third table on the page
        tables = await self.page.xpath("//table")
        table = tables[2]  # Get the third table

        column_names = ["SKU", "Description", "UOM", "Special Order", "Qty Ordered"]

        # Find the table rows
        row_elements = await table.xpath("./tbody/tr")

        # Initialize a list to store the extracted order items
        order_items = []

        # Iterate over each row and extract the data
        for row_element in row_elements:
            # Find the cells within the row
            cell_elements = await row_element.xpath("./td")

            # Extract the values from each cell
            row_data = [await self.page.evaluate('(e) => e.textContent', cell_element) for cell_element in cell_elements]

            # Create a dictionary with column names as keys and row values as values
            row_dict = {column_names[i]: row_data[i] for i in range(len(column_names))}

            # Add the row data to the list
            order_items.append(row_dict)

        return order_items
