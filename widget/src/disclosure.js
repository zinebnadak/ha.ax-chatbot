export const AI_DISCLOSURE_SV = "Jag är en AI-assistent, inte en anställd på Högskolan på Åland.";
export const AI_DISCLOSURE_EN = "I am an AI assistant, not a staff member at Åland University of Applied Sciences.";

export function getDisclosure(language) {
  const lang = language.trim().toLowerCase();
  return lang.startsWith("sv") ? AI_DISCLOSURE_SV : AI_DISCLOSURE_EN;
}
