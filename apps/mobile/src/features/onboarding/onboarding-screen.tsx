import { useRouter } from 'expo-router';
import * as React from 'react';

import {
  Button,
  FocusAwareStatusBar,
  SafeAreaView,
  Text,
  View,
} from '@/components/ui';
import { useIsFirstTime } from '@/lib/hooks';
import { Cover } from './components/cover';

export function OnboardingScreen() {
  const [_, setIsFirstTime] = useIsFirstTime();
  const router = useRouter();
  return (
    <View className="flex h-full items-center justify-center">
      <FocusAwareStatusBar />
      <View className="w-full flex-1">
        <Cover />
      </View>
      <View className="justify-end">
        <Text className="my-3 text-center text-5xl font-bold">
          Crop Doctor
        </Text>
        <Text className="mb-2 text-center text-lg text-gray-600">
          Detect crop diseases. Get advice in your language.
        </Text>

        <Text className="my-1 pt-6 text-left text-lg">
          Take a photo of a sick leaf
        </Text>
        <Text className="my-1 text-left text-lg">
          Get a likely diagnosis in seconds
        </Text>
        <Text className="my-1 text-left text-lg">
          Receive plain-language next steps
        </Text>
        <Text className="my-1 text-left text-lg">
          Connect to an extension worker when needed
        </Text>
      </View>
      <SafeAreaView className="mt-6">
        <Button
          label="Let's Get Started "
          onPress={() => {
            setIsFirstTime(false);
            router.replace('/login');
          }}
        />
      </SafeAreaView>
    </View>
  );
}
