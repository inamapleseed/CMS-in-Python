# CAREERS PAGE CMS
#### Video Demo:  https://youtu.be/PkVidt_L7do
#### Description:
My company has a very underdeveloped website where every content is hardcoded. And as a full-stack developer, this is beyond embarrassing. So, I developed this careers page content management system for my HR admin so that they can independently access and efficiently update job postings. Though this semester’s course will be over soon, I shall continue to improve and develop a full content management system for the whole website.

On the registration page, for restriction purposes, registrants are required to input the pre-made ‘admin registration code’ in order to successfully register, which I shall provide them when the website is up and running.

The files departments.html, index.html, and job.html, are used to display specific information. However, departments.html is yet to be used upon continuing on this project after this course, which shall display each department and act as a filter when the user clicks on a specific department name. Upon clicking a department name, the user shall be redirected to another page that consists only of job postings under the said department. While the pages create.html, login.html, and register.html, are files that contain forms that input data provided to the database. And as for the update.html, it allows the admin to edit the existing data on the database.

For non-admin users, they can only access pages that are read-only such as index.html, and job.html which is the inner job page, and once the apply button is functional, on click, they shall be redirected to a page that has a form where they can input the requested data and attach their CV.

The update.html and job.html contain identical information, and the only differences are: update.html can only be accessed by logged-in users aka admins, and that the contents in update.html are inside text boxes to allow updates.



For improvement, I need to work on overall styles, the department page as a redirect to the inner department page, alerts and warnings when the provided login details are incorrect, and confirmation pop-ups before proceeding to update or leave the job post page. Also, in script.js and index.html, there are two separate scripts for modal pop-ups. I shall look into this and see whether there is a possibility to compile all the scripts inside script.js for best practice application, or if using one script for modal is possible as well. In the database table of jobs, I shall add more data regarding the job posting such as salary, work setup, minimum requirements, and the like.

For development, in addition to my existing careers content management system, I will have to develop a whole backend system where the admin can edit and manage everything on the main website’s landing page, about page, contact page, founder page, footer section, navigation bar, logo, and everything else on the website. I must create a web design in order for me to know the placements and positioning of my content management elements before proceeding to develop the backend system.

Once finished, this shall be pushed live on our existing company website, pitched to my boss, and hope the approve it.
