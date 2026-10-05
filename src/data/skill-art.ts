export function skillArtSlug(id:string){
  return id.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9-]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}
export const skillArtPath=(characterId:string,id:string)=>`/assets/skills/${characterId}/${skillArtSlug(id)}.png`;
