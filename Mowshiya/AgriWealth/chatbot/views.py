import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


SYSTEM_PROMPT = """You are AgriBot, an expert agricultural assistant for AgriWealth platform.
You help farmers with:
1. Converting farm waste into valuable products (compost, biofertilizer, biogas, animal feed, etc.)
2. Farming best practices and tips
3. Identifying waste types and their potential uses
4. Market advice for selling agricultural waste
5. Sustainable farming techniques

Be concise, practical, and encouraging. Use simple language. 
When suggesting waste conversion, always mention the environmental and financial benefits.
"""


@login_required
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')


@login_required
def chatbot_api_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        api_key = settings.OPENAI_API_KEY
        if not api_key:
            # Fallback rule-based response if no API key
            response = get_fallback_response(user_message)
            return JsonResponse({'response': response})

        import openai
        client = openai.OpenAI(api_key=api_key)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h in history[-10:]:  # Keep last 10 messages for context
            messages.append({"role": h['role'], "content": h['content']})
        messages.append({"role": "user", "content": user_message})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        response = completion.choices[0].message.content
        return JsonResponse({'response': response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_fallback_response(message):
    """Rule-based fallback when no OpenAI key is available."""
    message_lower = message.lower()

    if any(w in message_lower for w in ['compost', 'composting']):
        return ("Composting is a great way to turn crop residues, vegetable waste, and animal manure "
                "into nutrient-rich fertilizer! Mix green (nitrogen-rich) and brown (carbon-rich) "
                "materials in a 1:3 ratio, keep moist, and turn weekly. Ready in 6-8 weeks.")

    if any(w in message_lower for w in ['biofertilizer', 'bio fertilizer']):
        return ("Biofertilizers use microorganisms to enrich soil nutrients. You can create them from "
                "crop residues by fermenting with beneficial bacteria. They improve soil health and "
                "reduce chemical fertilizer costs by up to 40%!")

    if any(w in message_lower for w in ['biogas', 'bioenergy', 'energy']):
        return ("Biogas can be produced from animal manure, crop waste, and food scraps through "
                "anaerobic digestion. A small biogas digester can provide cooking fuel for a family "
                "and the leftover slurry is an excellent fertilizer!")

    if any(w in message_lower for w in ['rice', 'paddy', 'straw']):
        return ("Rice straw can be converted into: mushroom growing substrate, animal feed (after "
                "treatment), compost, biochar, or biogas. Avoid burning it — that wastes valuable "
                "nutrients and pollutes the air!")

    if any(w in message_lower for w in ['sell', 'price', 'market', 'buyer']):
        return ("To get the best price for your agricultural waste: list it on the AgriWealth "
                "marketplace with clear descriptions, mention possible end-uses, and price it "
                "competitively. Processed waste (compost, biofertilizer) fetches 3-5x more than raw waste!")

    if any(w in message_lower for w in ['hello', 'hi', 'hey', 'help']):
        return ("Hello! I'm AgriBot, your agricultural assistant. I can help you with:\n"
                "• Converting farm waste to compost, biofertilizer, or biogas\n"
                "• Farming tips and best practices\n"
                "• Pricing and selling your waste products\n"
                "What would you like to know?")

    return ("That's a great question! For the best advice on this topic, I recommend:\n"
            "1. Consulting with your local agricultural extension office\n"
            "2. Checking the AgriWealth marketplace for similar products\n"
            "3. Asking fellow farmers in your network\n"
            "Feel free to ask me about waste conversion, composting, biofertilizers, or biogas!")
