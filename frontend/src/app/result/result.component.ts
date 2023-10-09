import {Component, Input, OnInit} from '@angular/core';
import {DiffWord} from './diffword';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  @Input() response: {
    original_email: string,
    suggestions: Array<{
      sentence: string,
      diff: Array<string>,
    }>
  } | null = null;

  // @ts-ignore
  formattedEmail: DiffWord[][];

  ngOnInit() {
    this.formattedEmail = this.getFormattedEmail();
  }

  getFormattedEmail(): DiffWord[][] {
    const sentenceToDiffMap: { [key: string]: string[] } = {};
    this.response!.suggestions.forEach(suggestion => {
      sentenceToDiffMap[suggestion.sentence] = suggestion.diff;
    });

    const lines = this.response!.original_email.split('\n');
    const results: DiffWord[][] = lines.map(line => {
      const sentences = line.split(/(?<=[.!?])\s+/);
      let lineDiffWords: DiffWord[] = [];

      sentences.forEach(sentence => {
        const words = sentence.split(' ');
        const sentenceDiffs = sentenceToDiffMap[sentence] || [];

        let cursorWords = 0;
        sentenceDiffs.forEach(diff => {
          console.log(diff)
          if (diff.startsWith('+')) {
            lineDiffWords.push({ value: diff.slice(2), type: 'added' });
          } else if (diff.startsWith('-')) {
            const wordToRemove = diff.slice(2);
            const idx = words.indexOf(wordToRemove, cursorWords); // Find the word from cursor position
            if (idx !== -1) {
              lineDiffWords.push({ value: wordToRemove, type: 'removed' });
              cursorWords = idx + 1;
            }
          } else {
            lineDiffWords.push({ value: diff, type: 'unchanged' });
            cursorWords++;
          }
        });

        // Append any remaining unchanged words from the original text
        for (let i = cursorWords; i < words.length; i++) {
          lineDiffWords.push({ value: words[i], type: 'unchanged' });
        }
      });

      console.log(lineDiffWords)
      return lineDiffWords;
    });

    return results;
  }

  strip(word: string): string {
    return word.replace(/^[+\-]!\s?/, '').trim();
  }

  getDiffState(diff: string): string {
    return diff.startsWith('+') ? 'added' : diff.startsWith('-') ? 'removed' : 'unchanged';
  }

}
