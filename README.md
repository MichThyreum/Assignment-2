# Assignment-2 Build an AI-powered tool capable of performing a discrete legal or legal-adjacent task of your choosing.

The Legal Task this tool seeks to undertake: Under the Victorian Freedom of Information Act 1982 (Vic), anyone can ask to see documents that are held by agencies in the Victorian public sector. This tool helps staff upload documents that customers have asked for, usually about investigations into their tax matters. Once the documents are uploaded, the tool reviews them to check which parts must be shared and which parts do not have to be shared because of the Act. The tool clearly points out which sections are exempt from release and explains which rules or exemptions apply. After this review, staff can use the tool’s analysis to help make the final decision about what information can be given to the customer.

URL to your deployed application : 

URL to GitHub Repository: 

Source of Code: Claude ai

Test case to demonstrate the application’s functionality:

Step 1: The landing page of the application details how the FOI Case Management Tool works. 

Step 2: The navigation tab on the left of the application screen as three radio buttons. The Home button contains details on how to use FOI Case Management Tool.

Step 3: Click on the “Analyzer” button on the navigation tab on the left of the application screen.

Step 4: check on the “Show API key” checkbox. 

Step 5: Type your API key in the text box under “OpenAI API Key:” and click enter.

Step 6: Enter the customer name under “Step 1: Customer Names”. Enter the following:
Customer 1 - First Name: John 
Customer 1 – Last Name: Scape 

Step 7: Check the box next to “Add second customer”

Step 8: Enter the following:
Customer 1 - First Name: Ann
Customer 1 – Last Name: Scape 

Step 9: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button. 

Step 10: Test Case 1: Upload Investigation Letters. 

Step 11: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Investigation Commencement Letter and Investigation Outcome Letter. 

Step 12: Click the “Analyze Documents” button.

Step 13: The Analysis Results should state “Document 1: Investigation Commencement Letter.pdf RELEASE IN FULL - Document is a letter”. This is because the FOI request is being made by the customers listed in the customer names section of the application and can be released to the customer as the letters are addressed to the customers named. 
Despite the document being released in full an exemption analysis is performed on the letters based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

Step 14: The Analysis Results should state “Document 2: Investigation Outcome Letter.pdf RELEASE IN FULL - Document is a letter”. This is because the FOI request is being made by the customers listed in the customer names section of the application and can be released to the customer as the letters are addressed to the customers named.  
Despite the document being released in full an exemption analysis is performed on the letters based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

Step 15: Download Analysis (JSON) button can be clicked and viewed on notepad or word. 

Step 16: Click New to clear the analysis or click the clear button to clear the analysis. 

Step 17: Click the “x” button next to the two documents under the Browse files button.

Step 18: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button. 

Step 19: Test Case 2: Upload the internal investigation documents.  

Step 20: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Investigation Time Sheet and Investigation Report. 

Step 21: Click the “Analyze Documents” button.

Step 22: The Analysis Results should state “Document 1: Investigation Report.pdf REVIEW REQUIRED - 5 exemptions”. This is because this an internal office document that cannot be released in full to the customer.  
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

Step 23: The Analysis Results should state “Document 2: Investigation Time Sheet.pdf REVIEW REQUIRED - 8 exemptions”. This is because this an internal office document that cannot be released in full to the customer.   
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

Step 24: Click New to clear the analysis or click the clear button to clear the analysis. 

Step 25: Click the “x” button next to the two documents under the Browse files button.

Step 26: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button. 

Step 27: Test Case 3: Upload the Principal Place of Residence Exemption Guide.  

Step 28: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Principal Place of Residence Exemption Guide. 

Step 29: Click the “Analyze Documents” button.

Step 30: The Analysis Results should state “Document 1: Principal Place of Residence Exemption Guide.pdf REVIEW REQUIRED - 5 exemptions”. This is because this an internal office document that cannot be released in full to the customer.   
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

