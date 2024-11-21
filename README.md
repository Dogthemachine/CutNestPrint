![Cut Nest Print Logo](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/CNP_logo-100.png)

# Cut Nest Print

## Unique Automated Solution for Optimizing the Layout of Fabric Patterns

A pipeline allowing shop administrators to compose production orders using the existing stock and delivery management interface, bypassing complex procedures and simplifying the workflow.

### Shares Product Database with the [Website](https://catcult.club/)

---

![Product Database Integration](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/1.png)

The application shares the same product database used for stock and delivery administration, allowing the shop administrator to seamlessly use familiar interfaces to place production orders.

---

![Adding Products to Orders](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/2.png)

The administrator can add specific products to the production order, selecting items and sizes directly from the existing product database. This makes order management straightforward and avoids duplicating data entry.

---

![Pattern Association](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/3.jpeg)

Each product has associated patterns that need to be cut from fabric. These patterns are stored and managed within the application, allowing easy access when processing orders.

---

![DeepNest Integration](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/5.png)

Once an order is completed, all patterns associated with the products in the order are traced by the **OpenCV** library to convert them to **SVG vector format**. The traced SVG files are passed to the **DeepNest** application, which has been modified to take input from a specified folder and export a **JSON file** containing coordinates, instead of an SVG file, after finding the most efficient placement for pattern details on the fabric.

---

![Final Layout Generation](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/8.jpeg)

Using the JSON file containing coordinates and rotation angles, the **Cut Nest Print** application places all patterns from the order into a **final TIFF file** ready for printing. The **Pillow** library is used to ensure precise placement, creating a production-ready fabric layout. Once the final TIFF file is generated, it is uploaded to the cloud, and an email notification is automatically sent to the production team with a download link to access the file, ensuring a smooth transition from digital preparation to physical production.

---

## Summary

Cut Nest Print automates the traditionally manual and time-consuming process of arranging fabric patterns for production. This system uses **OpenCV** and **DeepNest** to ensure efficient pattern placement, drastically reducing fabric waste and production time. By integrating this solution into the existing Django-based shop management interface, Cut Nest Print simplifies order creation, optimizes the use of materials, and delivers fully prepared production files ready for printing.
