from django.http import JsonResponse
import google.generativeai as genai
from salon_site.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

SALON_PROMPT = """
You are the assistant for Royal Barber Salon.
Salon details:
- Services: Haircuts, beard trim and Styling, shaving, facial, kids cut, groom packages, hair colour, hair wash.
- Prices: Haircut ₹199 duration 25 min, Beard trim and Styling Rs.199 duration 20 min, Facial Rs.499 duration 30min, Hair wash Rs.199 duration 20min,Shaving Rs.199 duration 20min, Hair colour Rs.399 duration 40min, kids hair cut Rs.149 duration 20min, Groom package Rs.9999 duration 2 hour.
- Timings: Monday-Sunday 10:00am - 9:00pm.
- Address: Shop No.2,Numaish Camp, Saharanpur,247001. Parking available.
- Contact: 99999-88888.
- Booking Process- Contact Use or First login-> service add to cart->select time and slot-> make payment.
- Cacellation Process- cancel will taken only before 1 day from booking date. Go to My booking and then click Cancel. You refund will be initated.
- No Home service.
- walkin also allowed. but priority given to booking customer.
Rules:
- If not salon related → reply: "Please ask only salon related queries."
- If salon related but not in details → reply: "Please contact us directly at 99999-88888 for details."
"""

def ask_ai(request):
    import json
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "")

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(f"{SALON_PROMPT}\nUser: {user_msg}")
            answer = response.text.strip()
            return JsonResponse({"success": True, "answer": answer})
        except Exception as e:
            return JsonResponse({"success": False, "answer": "Error: " + str(e)})

    return JsonResponse({"success": False, "answer": "Invalid request"})
