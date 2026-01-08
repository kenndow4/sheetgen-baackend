from src.config.ia import client
import json

SYSTEM_PROMPT = """
You are a JSON generator for Excel structures.

OUTPUT FORMAT:
{
  "columns": ["Column1", "Column2"],
  "rows": [
    ["value1", "value2"],
    ["value3", "value4"]
  ],
  "header_style": {
    "bg_color": "4472C4",
    "font_color": "FFFFFF",
    "bold": true,
    "font_size": 12,
    "alignment": "center"
  },
  "column_configs": [
    {"name": "Column1", "width": 20, "style": {"alignment": "center"}}
  ]
}

RULES:
1. Output ONE JSON object only
2. Start with { and end with }
3. NO multiple JSON objects
4. NO markdown, NO explanations
5. Generate 5-10 realistic sample rows
6. Colors are HEX without # (e.g., "4472C4" for blue)
7. Professional styling when requested

Common colors:
- Dark blue: 00008B or 4472C4
- Navy: 000080
- Green: 008000 or 70AD47
- Gray: E7E6E6
- White: FFFFFF
"""

def generate_excel_structure(prompt: str) -> dict:
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        raw = completion.choices[0].message.content.strip()
        print(f"Raw IA Response:\n{raw}\n")
        
     
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        
        lines = raw.split('\n')
        json_lines = []
        brace_count = 0
        started = False
        
        for line in lines:
            for char in line:
                if char == '{':
                    brace_count += 1
                    started = True
                elif char == '}':
                    brace_count -= 1
            
            if started:
                json_lines.append(line)
            
          
            if started and brace_count == 0:
                break
        
        raw = '\n'.join(json_lines)
        print(f"📦 Extracted first JSON:\n{raw}\n")
        
        parsed = json.loads(raw)
        
        # Detectar wrappers
        if "excel_structure" in parsed:
            print("⚠️ Detected wrapper 'excel_structure', extracting...")
            parsed = parsed["excel_structure"]
        
        # Validar campos requeridos
        if "columns" not in parsed:
            print(f"❌ Missing 'columns'. Available keys: {list(parsed.keys())}")
            raise ValueError("Missing required field: 'columns'")
        
        if "rows" not in parsed:
            print(f"❌ Missing 'rows'. Available keys: {list(parsed.keys())}")
            raise ValueError("Missing required field: 'rows'")
        
        print(f"✅ Parsed successfully: {len(parsed['columns'])} columns, {len(parsed['rows'])} rows")
        return parsed
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        print(f"Raw response was:\n{raw}")
        raise ValueError(f"IA returned invalid JSON: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise