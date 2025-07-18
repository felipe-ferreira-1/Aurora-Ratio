def listar_missoes(supabase):
  return supabase.table("missoes").select("*").execute().data

def progresso_do_usuario(email, supabase):
  registros = supabase.table("progresso_missoes").select("missao_id").eq("email", email).execute().data
  return [r["missao_id"] for r in registros]

def registrar_progresso(email, missao_id, supabase):
  supabase.table("progresso_missoes").insert({
      "email": email,
      "missao_id": missao_id
  }).execute()