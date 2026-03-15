הוראות למי שרוצה להשתמש:
1. שימו את הקבצים האלה תחת אותה תיקייה במחשב שלכם

תיצרו תחת אותה תיקייה תיקיות בשם testing-oracle ו-testing-odbc. העתיקו לתוך כל אחד מהם את קובץ הדמה המתאים שעדו הכניס.

תרימו עם הפקודה docker-compose up --build

בקשות לדוגמא:

GET:

curl -v -u informatikit -H "If-Modified-Since: <timestamp>" http://localhost:8080/oracle/network/admin/tnsnames.ora

PUT:

curl -u informatikit -T testing-oracle/tnsnames-new.ora -i http://localhost:8080/oracle/network/admin/tnsnames.ora

דגשים:

ה-timestamp בפקודה של ה-get חייבת להיות זהה לחלוטין ל-timestamp האחרון שיש לכם מ-header של בקשה. אחרת זה ידפיס לכם את הקובץ גם אם הוא לא שונה מפעם אחרונה.

בגלל החיבור ב-mount, לערוך את הקובץ במחשב זה כמו לערוך בקונטיינר. אתם יכולים להיעזר בזה כדי לבדוק timestamp וכאלה. אבל אם אתם רוצים לעשות put תיצרו עותק במחשב שלכם, תעשו עליו שינויים ותשלחו אותו בבקשה.
