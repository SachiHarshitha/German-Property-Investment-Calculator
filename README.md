# German-Property-Investment-Calculator
Static, browser-only dashboard that simulates property investment gains (including simplified German tax estimates) without any backend server.

## Running the app
- Open `templates/index.html` directly in your browser, or
- Serve the repository with a static server (e.g., `python -m http.server`) and visit `http://localhost:8000/templates/`.

### Rebuilding the frontend (TypeScript)
```
npm install
npm run build
```
The compiled output is written to `static/js/app.js`, which `templates/index.html` already loads.

## User Input
User Input in this app is seperated under 6 sections.

### 1.Personal Information
![image](https://github.com/user-attachments/assets/d4043266-37e5-434f-8f89-f34e312ba473)

### 2.Apartment Details
![image](https://github.com/user-attachments/assets/5fd5635d-6e07-4148-9a9a-ab08bb1fe8c3)

### 3.Rental Details
![image](https://github.com/user-attachments/assets/1ee19442-58fb-4b62-bf3d-8d9fbcfd4799)

### 4.Purchase Costs
![image](https://github.com/user-attachments/assets/00f3ed03-e67f-4402-a14c-82b69d1681ae)

### 5.Mortgage Values
![image](https://github.com/user-attachments/assets/24f8d605-0315-46cd-ae80-c685fdd0e33c)

### 6.Other Settings
![image](https://github.com/user-attachments/assets/61c55c45-b248-4036-8cae-44498ad8533f)

### 7. Furnishing Settings
Using this section the user may calculate the furniture depreciation.
![image](https://github.com/user-attachments/assets/ecbdd62c-5f47-4cb9-a9f5-6df633ea5b01)

#### 7.1 Set Depreciation Years
![image](https://github.com/user-attachments/assets/b23bb5b1-7b28-4140-bc07-82415e761731)

#### 7.2 Insert Different Furniture Items
![image](https://github.com/user-attachments/assets/af77caea-71fb-4158-9c70-a06915ba5989)


### Simulation Output
![image](https://github.com/user-attachments/assets/c5397e78-b031-43a1-ace5-882ddcf6ffd9)

#### Statistics
![image](https://github.com/user-attachments/assets/abd12b99-463c-42c5-9d8b-c8114bce73de)

