import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {

  @Input() response: {
    original_email: string,
    suggestions: Array<{
      sentence: string,
      diff: Array<string>,
    }>
  } | null = null;

  get original_email(): string {
    return this.response?.original_email || '';
  }

  splitSentences(email: string): string[] {
    // Splitting by sentence using regex; note that this is a simple split and may not handle all cases
    return email.match(/[^\.!\?]+[\.!\?]+/g) || [];
  }

  getSuggestion(sentence: string): any {
    return this.response?.suggestions.find(s => s.sentence.trim() === sentence.trim()) || null;
  }
}
