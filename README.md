![Cut Nest Print Logo](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/CNP_logo-100.png)

# Cut Nest Print

## Unique Automated Solution for Optimizing the Layout of Fabric Patterns

Cut Nest Print is an automated solution designed to streamline the process of creating fabric patterns for clothing production. It allows shop administrators to compose production orders using the existing stock and delivery management interface, bypassing complex procedures and simplifying the entire workflow. The solution is integrated with the [website](https://catcult.club/), sharing a product database for efficiency.

### Workflow Overview

**Product Database Integration**

   ![Product Database Integration](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/1.png)

   The application shares the same product database used for stock and delivery administration, allowing the shop administrator to seamlessly use familiar interfaces to place production orders.

**Adding Products to Orders**

   ![Adding Products to Orders](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/2.png)

   The administrator can add specific products to the production order, selecting items and sizes directly from the existing product database. This makes order management straightforward and avoids duplicating data entry.

**Associated Pattern Details**

   ![Pattern Association](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/3.jpeg)

   Each product has associated patterns that need to be cut from fabric. These patterns are stored and managed within the application, allowing easy access when processing orders.

**Pattern Tracing with OpenCV**

   ![Pattern Tracing](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/4.png)

   Once an order is completed, all patterns associated with the products in the order are traced by the **OpenCV** library to convert them to **SVG vector format**. This process ensures high precision for subsequent pattern layout.

**DeepNest Integration for Optimal Pattern Placement**

   ![DeepNest Integration](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/5.png)

   The traced SVG files are passed to the **DeepNest** application. DeepNest has been modified to take input from a specified folder and export a **JSON file** containing coordinates, instead of an SVG file, after finding the most efficient placement for pattern details on the fabric.

**Finding Optimal Pattern Layout**

   ![Optimal Pattern Layout](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/6.jpeg)

   DeepNest's algorithm calculates the best arrangement for all pattern pieces to minimize fabric usage and reduce waste. When the optimal placement is found, DeepNest exports the layout information as a JSON file.

**Final Production File Creation**

   ![Final Layout Generation](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/7.png)

   Using the JSON file containing coordinates and rotation angles, the **Cut Nest Print** application places all patterns from the order into a **final TIFF file** ready for printing. The **Pillow** library is used to ensure precise placement, creating a production-ready fabric layout.

**Uploading and Notification**

   ![Cloud Upload](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/8.jpeg)

   Once the final TIFF file is generated, it is uploaded to the cloud. An email notification is automatically sent to the production team with a download link to access the file, ensuring a smooth transition from digital preparation to physical production.

**Order Tracking and Management**

   ![Order Tracking](https://github.com/Dogthemachine/CutNestPrint/blob/master/assets/img/9.png)

   The system allows administrators to track orders, including details such as fabric used, quantity, and production status, ensuring all aspects of production are effectively managed.


Cut Nest Print automates the traditionally manual and time-consuming process of arranging fabric patterns for production. This system uses **OpenCV** and **DeepNest** to ensure efficient pattern placement, drastically reducing fabric waste and production time. By integrating this solution into the existing Django-based shop management interface, Cut Nest Print simplifies order creation, optimizes the use of materials, and delivers fully prepared production files ready for printing.
