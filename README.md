# Assignment-2 Build an AI-powered tool capable of performing a discrete legal or legal-adjacent task of your choosing.

The Legal Task this tool seeks to undertake: Under the Victorian Freedom of Information Act 1982 (Vic), anyone can ask to see documents that are held by agencies in the Victorian public sector. This tool helps staff upload documents that customers have asked for, usually about investigations into their tax matters. Once the documents are uploaded, the tool reviews them to check which parts must be shared and which parts do not have to be shared because of the Act. The tool clearly points out which sections are exempt from release and explains which rules or exemptions apply. After this review, staff can use the tool’s analysis to help make the final decision about what information can be given to the customer.

URL to your deployed application : https://assignment-2-rmr2gzjj27utml6j2umyx5.streamlit.app/

URL to GitHub Repository:https://reimagined-halibut-g4w9vw4pp6wqhvwj5.github.dev/

Source of Code: Claude ai

Test case to demonstrate the application’s functionality:

Step 1: The landing page of the application details how the FOI Case Management Tool works.

Step 2: The navigation tab on the left of the application screen has three radio buttons. The Home button contains details on how to use FOI Case Management Tool.

Step 3: Click on the “Analyser” button on the navigation tab on the left of the application screen.

Step 4: Check on the “Show API key” checkbox.

Step 5: Type your API key in the text box under “OpenAI API Key:” and click enter.

Step 6: Enter the customer name under “Step 1: Customer Names”. Enter the following:
Customer 1 - First Name: John
Customer 1 – Last Name: Scape

Step 7: Check the box next to “Add second customer”

Step 8: Enter the following:
Customer 1 - First Name: Ann
Customer 1 – Last Name: Scape

Step 9: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button. 
Please note the Test case documents are available in the GitHub Code.  To download these documents please click on the Test Case Documents folder on the github code space, this will list all 5 documents that are part of the test case. Right click each file and press download on each document. Save these documents in a place they can be accessed easily. 

Step 10: Test Case 1: Upload Investigation Letters (documents titled Investigation Outcome Letter and Investigation Commencement Letter).

Step 11: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Investigation Commencement Letter and Investigation Outcome Letter.

Step 12: Click the “Analyse Documents” button.

Step 13: The screen should display “Loading reference documents” and “Loaded 3 reference documents” this shows that the 3 reference documents are being analysed.

Step 14: The Analysis Results should state “Document 1: Investigation Commencement Letter.pdf RELEASE IN FULL - Document is a letter”. This is because the FOI request is being made by the customers listed in the customer names section of the application and can be released to the customer as the letters are addressed to the customers named.
Despite the document being released in full an exemption analysis is performed on the letters based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions.

Step 15: The Analysis Results should state “Document 2: Investigation Outcome Letter.pdf RELEASE IN FULL - Document is a letter”. This is because the FOI request is being made by the customers listed in the customer names section of the application and can be released to the customer as the letters are addressed to the customers named.  
Despite the document being released in full an exemption analysis is performed on the letters based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions.

Step 16: Download Analysis (JSON) button can be clicked and viewed on notepad or word.

Step 17: Click “New” to clear the analysis or click the “Clear” button to clear the analysis.

Step 18: Click the “x” button next to the two documents under the Browse files button.

Step 19: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button.

Step 20: Test Case 2: Upload the internal investigation documents.  

Step 21: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Investigation Time Sheet and Investigation Report.

Step 22: Click the “Analyse Documents” button. The screen should display “Loading reference documents” and “Loaded 3 reference documents” this shows that the 3 reference documents are being analysed.

Step 23: The Analysis Results should state “Document 1: Investigation Report.pdf REVIEW REQUIRED - 5 exemptions”. This is because this an internal office document that cannot be released in full to the customer.  
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions. 

Step 24: The Analysis Results should state “Document 2: Investigation Time Sheet.pdf REVIEW REQUIRED - 8 exemptions”. This is because this an internal office document that cannot be released in full to the customer.  
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions.
Download Analysis (JSON) button can be clicked and viewed on notepad or word.

Step 25: Click New to clear the analysis or click the clear button to clear the analysis.

Step 26: Click the “x” button next to the two documents under the Browse files button.

Step 27: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button.

Step 28: Test Case 3: Upload the Principal Place of Residence Exemption Guide.  

Step 29: Under “Step 2: Upload Documents (up to 2)” click on the “Browse Files” button and add Principal Place of Residence Exemption Guide.

Step 30: Click the “Analyse Documents” button. The screen should display “Loading reference documents” and “Loaded 3 reference documents” this shows that the 3 reference documents are being analysed.

Step 31: The Analysis Results should state “Document 1: Principal Place of Residence Exemption Guide.pdf REVIEW REQUIRED - 5 exemptions”. This is because this an internal office document that cannot be released in full to the customer.  
A full an exemption analysis is performed on the document based on the FOI exemptions, FOI guidelines and Taxation Administration Act documents.  The Executive Summary: Exemptions Analysis and has a breakdown of the exemptions” and the Exemptions section lists the exemptions.
Download Analysis (JSON) button can be clicked and viewed on notepad or word.


